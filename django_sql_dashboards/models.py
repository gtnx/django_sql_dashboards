from django.db import models
from django.template import Context, loader
from db import DB

class DbConfig(models.Model):
  name = models.CharField(max_length = 255)
  host = models.CharField(max_length = 255)
  user = models.CharField(max_length = 255)
  passwd = models.CharField(max_length = 255)
  db = models.CharField(max_length = 255)

  ts_create = models.DateTimeField(auto_now_add = True)
  ts_update = models.DateTimeField(auto_now_add = True, auto_now = True)

  class Meta:
    ordering = ["name"]
    
  def getDb(self):
    return DB(host = self.host, user = self.user, passwd = self.passwd, db = self.db)

  def __unicode__(self):
    return "%s@%s:%s" % (self.user, self.host, self.db)

class Query(models.Model):
  db = models.ForeignKey(DbConfig)
  title = models.CharField(max_length = 255, blank = True)
  subtitle = models.CharField(max_length = 255, blank = True)
  xlegend = models.CharField(max_length = 255, blank = True)
  ylegend = models.CharField(max_length = 255, blank = True)
  type = models.CharField(max_length = 255, choices = (('line', 'Line Chart'), 
                                                       ('area', 'Area Chart'), 
                                                       ('column', 'Column Chart'),
                                                       ('bar', 'Bar Chart')))
  query = models.TextField(blank = True)
  
  def execute(self):
    return self.db.getDb().hquery(self.query)

  def getAll(self):
    data, headers = self.execute()
    obj = {"title": self.title,
           "subtitle": self.subtitle,
           "xlegend": self.xlegend,
           "ylegend": self.ylegend,
           "type": self.type}
    obj["categories"] = [i[0] for i in data]
    obj["series"] = [{"name": headers[i], "data": [row[i] for row in data]} for i in range(1, len(headers))]
    return data, headers, obj

  def __unicode__(self):
    return self.title

  def toHighcharts(self):
    id_div = "id_query_%s" % self.id
    obj = self.getAll()[2]
    return loader.get_template('django_sql_dashboards/highcharts.html').render(Context(locals()))

class Dashboard(models.Model):
  title = models.CharField(max_length = 255, blank = True)
  column_nb = models.IntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (6, 6)))

  def __unicode__(self):
    return self.title

  def getColumnSize(self):
    return 12/self.column_nb

  def queries(self):
    return [i.query for i in self.dashboardquery_set.all().order_by("order_id")]

class DashboardQuery(models.Model):
  dashboard = models.ForeignKey(Dashboard)
  query = models.ForeignKey(Query)
  order_id = models.IntegerField()

  class Meta:
    unique_together = ["dashboard", "query"]