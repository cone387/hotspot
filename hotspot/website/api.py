# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-20 16:07
# software: PyCharm
from django.forms import model_to_dict
from django.views.generic import View, ListView
from .models import SourceItem, HotSpot
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.shortcuts import get_object_or_404
from .response import ApiResponse
from django.views.decorators.csrf import csrf_exempt


# api.seekcone.com/spider/config/get_next
# api.seekcone.com/spider/config/get_by_id
class SpiderSchedule(View):

    def get(self, request):
        data = None
        id = request.GET.get('id')
        if id:
            try:
                data = model_to_dict(SourceItem.objects.get(id=id))
            except:
                pass
        else:
            source_list = SourceItem.objects.filter(fetch_time__lte=now())
            if source_list:
                source = source_list[0]
                source.fetch_time = source.fetch_time + timedelta(minutes=source.fetch_interval)
                source.save()
                data = model_to_dict(source)
        return ApiResponse(data=data)


class DataFetcher(ListView):
    paginate_by = 10
    model = HotSpot
    ordering = '-id'

    def get_queryset(self):
        id = self.request.GET.get('id')
        if not id:
            return []
        try:
            source: SourceItem = SourceItem.objects.get(id=id)
        except:
            return []
        self.paginate_by = source.default_count
        return HotSpot.objects.filter(source=source.id)\
            .order_by(self.ordering).values('real_pos', 'title', 'url', 'hot_descr')

    def render_to_response(self, context, **response_kwargs):
        return ApiResponse(data=list(context['object_list']))


def get_enable_website(request):    # 已启用的采集
    category = request.GET.get('category')
    if category:
        site_list = SourceItem.objects.filter(status=1, category=category)
    else:
        site_list = SourceItem.objects.filter(status=1)
    site_list = site_list.values('id', 'name', 'url', 'category', 'site_name', 'image')
    return ApiResponse(data=list(site_list))


def get_crawl_time(request):    # 获取网站的最近更新时间
    if request.method != 'GET':
        return ApiResponse(success=False, code=500, data="method not allow")
    id = request.GET.get('id')
    if not id:
        return ApiResponse("get failed, the source does't exists", code=400)
    try:
        source = SourceItem.objects.get(id=id)
    except:
        return ApiResponse("get failed, the source does't exists", code=400)
    return ApiResponse(data=model_to_dict(source, fields=['id', 'name', 'last_runtime']))


@csrf_exempt
def update_website(request):    # 更新配置的异常，与采集时间
    id = request.POST.get('id')
    if not id:
        return ApiResponse(data="update failed, the source does't exists", code=400)
    try:
        source: SourceItem = SourceItem.objects.get(id=id)
    except:
        return ApiResponse(data="update failed, the source does't exists", code=400)
    abnormal = request.POST.get('abnormal')
    warn_msg = request.POST.get('warn_msg')
    try:
        run_time: float = datetime.fromtimestamp(request.POST.get('run_time')).strftime('%Y-%m-%d %H:%M:%S')
        source.last_runtime = run_time
        if abnormal:
            source.abnormal = abnormal
            source.warn_msg = warn_msg
        source.save()
        return ApiResponse(data='update success')
    except Exception as e:
        return ApiResponse(success=False, data=str(e))
