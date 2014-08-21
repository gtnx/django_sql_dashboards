import pickle
import datetime
import logging
import decimal
from dateutil import tz

from django.db import models
from django.template import Context, loader
from db import DB
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

logger = logging.getLogger("sql-dashboards")

class DbConfig(models.Model):
  name = models.CharField(max_length = 255, primary_key = True)
  host = models.CharField(max_length = 255)
  user = models.CharField(max_length = 255)
  passwd = models.CharField(max_length = 255)
  db = models.CharField(max_length = 255)

  ts_create = models.DateTimeField(auto_now_add = True)
  ts_update = models.DateTimeField(auto_now_add = True, auto_now = True)

  class Meta:
    ordering = ["name"]

  def getDb(self):
    return DB(host = self.host, user = self.user, \
              passwd = self.passwd, db = self.db)

  def __unicode__(self):
    return "%s (%s@%s:%s)" % (self.name, self.user, self.host, self.db)

class Query(models.Model):
  db = models.ForeignKey(DbConfig)
  title = models.CharField(max_length = 255)
  subtitle = models.CharField(max_length = 255, blank = True)
  xlegend = models.CharField(max_length = 255, blank = True)
  ylegend = models.CharField(max_length = 255, blank = True)
  type = models.CharField(max_length = 255, choices = (('table', 'Table'),
                                                       ('line', 'Line Chart'), 
                                                       ('area', 'Area Chart'), 
                                                       ('column', 'Column Chart'),
                                                       ('bar', 'Bar Chart')))
  query = models.TextField(blank = True)
  creator = models.ForeignKey(User)

  ts_create = models.DateTimeField(auto_now_add = True)
  ts_update = models.DateTimeField(auto_now_add = True, auto_now = True)

  public = models.BooleanField(default = True)

  legend_align = models.CharField(max_length = 64, default = 'right', choices = (('top', 'Top'), ('left', 'Left'), ('bottom', 'Bottom'), ('right', 'Right'), ))
  cache_ttl = models.IntegerField(default = 0, choices = ((0, "No cache"), (60, "1 minute"), (300, "5 minutes"), (3600, "1 hour"), (86400, "1 day"), (7*86400, "1 week")))

  custom = models.BooleanField(default = False)

  def __init__(self, *args, **kwargs):
    super(Query, self).__init__(*args, **kwargs)
    self.data, self.headers, self.obj = None, None, None

  def execute(self, custom_data = None, cached = True):
    if cached:
      history = QueryHistory.objects.filter(query = self).order_by("-ts_update")[:1]
      if len(history):
        if (datetime.datetime.now().replace(tzinfo=tz.tzlocal()) - history[0].ts_update).seconds <= self.cache_ttl:
          return pickle.loads(history[0].data)

    try:
      if self.custom:
        data = self.db.getDb().hquery(self.query % custom_data)
      else:
        data = self.db.getDb().hquery(self.query)
      if data:
        if self.id:
          QueryHistory.objects.filter(query = self).delete()
          QueryHistory(query = self, data = pickle.dumps(data)).save()
    except Exception as e:
      logger.error(str(e))
      return None
    return data

  def getAll(self, custom_data = None):
    ret = self.execute(custom_data = custom_data)
    if ret:
      self.data, self.headers = ret
      self.obj = {"title": self.title,
                  "subtitle": self.subtitle,
                  "xlegend": self.xlegend,
                  "ylegend": self.ylegend,
                  "type": self.type,
                  "legend_align": self.legend_align}
      self.obj["categories"] = [i[0] for i in self.data]
      self.obj["series"] = [{"name": self.headers[i], "data": [row[i] for row in self.data]} for i in range(1, len(self.headers))]

  def __unicode__(self):
    return self.title

  def toHighcharts(self):
    id_div = "id_query_%s" % self.id
    try:
      data, headers, obj = self.data, self.headers, self.obj
      if self.type == "table":
        return loader.get_template('django_sql_dashboards/table.html').render(Context(locals()))
      for serie in obj["series"]:
        for x in serie["data"]:
          if not isinstance(x, long) and not isinstance(x, decimal.Decimal) and not isinstance(x, float):
            raise Exception("Not properly formatted. Maybe null fields ?")
      return loader.get_template('django_sql_dashboards/highcharts.html').render(Context(locals()))
    except Exception as e:
      logger.error(str(e))
      return loader.get_template('django_sql_dashboards/query_error.html').render(Context(locals()))

  def toD3(self):
    id_div = "id_query_%s" % self.id
    data, headers, obj = self.getAll()
    if self.type == "table":
      return loader.get_template('django_sql_dashboards/table.html').render(Context(locals()))
    return loader.get_template('django_sql_dashboards/d3.html').render(Context(locals()))

class Dashboard(models.Model):
  title = models.CharField(max_length = 255, blank = True)
  column_nb = models.IntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (6, 6)))
  creator = models.ForeignKey(User)

  def __init__(self, *args, **kwargs):
    super(Dashboard, self).__init__(*args, **kwargs)
    self.queries = None
    
  def __unicode__(self):
    return self.title

  def getColumnSize(self):
    return 12/self.column_nb

  def getQueries(self):
    self.queries = [i.query for i in self.dashboardquery_set.all().order_by("order_id")]

class DashboardQuery(models.Model):
  dashboard = models.ForeignKey(Dashboard)
  query = models.ForeignKey(Query)
  order_id = models.IntegerField()

  class Meta:
    unique_together = ["dashboard", "query"]

class QueryHistory(models.Model):
  query = models.ForeignKey(Query)
  data = PickledObjectField()
  ts_create = models.DateTimeField(auto_now_add = True)
  ts_update = models.DateTimeField(auto_now_add = True, auto_now = True)
