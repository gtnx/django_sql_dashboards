from django.views.generic.list import ListView
from django.http import *
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, RequestContext
from django.db import connection, DatabaseError
from django.db.models import Max

from models import Query, Dashboard, DashboardQuery, DbConfig
from forms import QueryForm, QueryAddForm
from filters import QueryFilter, DashboardFilter

def default(request):
  return HttpResponseRedirect("/sql_dashboards", RequestContext(request))

def home(request):
  queries = Query.objects.all()
  dashboards = Dashboard.objects.all
  return render_to_response("django_sql_dashboards/home.html", locals(), RequestContext(request))  

def query_view(request):
  query_filter = QueryFilter(request.GET, queryset=Query.objects.all())
  return render_to_response("django_sql_dashboards/home.html", locals(), RequestContext(request))
  
def dashboard_view(request):
  dashboard_filter = DashboardFilter(request.GET, queryset=Dashboard.objects.all())
  return render_to_response("django_sql_dashboards/home.html", locals(), RequestContext(request))

def query_editor(request, query_id = None):
  form = QueryForm(request.POST) if request.method == 'POST' else QueryForm()
  query = None
  if query_id is not None:
    try:
      query = Query.objects.get(id = query_id)
    except:pass
    if not query:
      return HttpResponseRedirect("/sql_dashboards/query/")
  if request.method == "GET" and query_id is not None:
    form = QueryForm(instance = query)
  elif request.method == "POST" and ("run" in request.POST or "save" in request.POST):
    form = QueryForm(request.POST, instance = query) if query else QueryForm(request.POST) 
    if form.is_valid():
      query = form.save(commit = "save" in request.POST, user = request.user)

  if query:
    data, headers, obj = query.getAll()
  if request.method == "POST" and "save" in request.POST:
    return HttpResponseRedirect("/sql_dashboards/query/edit/%s" % query.id)
  return render_to_response("django_sql_dashboards/query_editor.html", locals(), RequestContext(request))

def dashboard_editor(request, dashboard_id = None):
  dashboard = None
  form = QueryAddForm()
  if request.method == "POST" and "add" in request.POST:
    form = QueryAddForm(request.POST)
    if form.is_valid():
      order_id = DashboardQuery.objects.filter(dashboard_id = dashboard_id).aggregate(Max('order_id'))["order_id__max"]
      order_id = order_id + 1 if order_id else 0
      try:
        dq = DashboardQuery.objects.get(query = form.cleaned_data["query"], dashboard_id = dashboard_id)
        dq.order_id = order_id
      except:
        dq = DashboardQuery(query = form.cleaned_data["query"], dashboard_id = dashboard_id, order_id = order_id)
      dq.save()

  form.fields["query"].queryset = Query.objects.exclude(dashboardquery__dashboard = dashboard_id)
  if dashboard_id:
    try:
      dashboard = Dashboard.objects.get(id = dashboard_id)
    except Exception as e:
      print(str(e))
      return HttpResponseRedirect("/sql_dashboards/dashboard")
  return render_to_response("django_sql_dashboards/dashboard_editor.html", locals(), RequestContext(request))

def dashboard_delete_query(request, dashboard_id, query_id):
  try:
    dashboard = Dashboard.objects.get(id = dashboard_id)
    if dashboard.creator == request.user:
      DashboardQuery.objects.filter(dashboard_id = dashboard_id, query_id = query_id).delete()
  except Exception as e:
    print(str(e))
  return HttpResponseRedirect("/sql_dashboards/dashboard/edit/%s" % dashboard_id)

def dashboard_editor_change_order(request, dashboard_id = None):
  dashboard = None
  if dashboard_id:
    try:
      dashboard = Dashboard.objects.get(id = dashboard_id)
      for i, query_id in enumerate(request.GET.get("order", "").split(",")):
        dq = DashboardQuery.objects.get_or_create(dashboard = dashboard, query_id = query_id)[0]
        dq.order_id = i
        dq.save()
    except Exception as e:
      print(str(e))
  return HttpResponse("")

def to_highcharts(request, query_id):
  try:
    return HttpResponse(Query.objects.get(id = query_id).toHighcharts())
  except Exception as e:
    return HttpResponse(str(e), status = 202)

def test_query(request):
  response_data = {}
  try:
    cursor = DbConfig.objects.get(id = int(request.GET.get("db"))).getDb().curs
    cursor.execute("explain %s" % request.GET.get("query",""))
    row = cursor.fetchone()
    response_data["data"] = dict([(cursor.description[i][0], row[i]) for i in range(len(cursor.description))])
  except DatabaseError as e:
    response_data["error"] = str(e)
  except Exception as e:
    response_data["error"] = str(e)
  response = render_to_response("django_sql_dashboards/test_query.html", response_data, RequestContext(request))
  response.status_code = status = 202 if "error" in response_data else 200
  return response

