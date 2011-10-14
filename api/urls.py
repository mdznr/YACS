from django.conf.urls.defaults import patterns, include, url
from timetable.courses.models import Section
from timetable.api.resources import (dept_handler, semester_handler, bulk_course_handler,
    course_handler, section_handler, schedule_handler, compute_schedule_handler, period_handler)

defaults = {'emitter_format': 'json', 'version': 1}
defaults_study_abroad = {'emitter_format': defaults['emitter_format'], 'number': Section.STUDY_ABROAD, 'version': 1}

urlpatterns = patterns('',
    ## Data APIs ##
    # narrowing by semester
    url(r'^$', semester_handler, defaults, name='semesters'),
    url(r'^(?P<year>\d{4})/$', semester_handler, defaults, name='semesters-by-year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', semester_handler, defaults, name='semester'),
    # or courses
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/courses/$', bulk_course_handler, defaults, name='courses-by-semester'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/courses/(?P<cid>\d+)/$', course_handler, defaults, name='course-by-id'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/courses/(?P<cid>\d+)/sections/$', section_handler, defaults, name='sections'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/courses/(?P<cid>\d+)/sections/(?P<number>\d+)/$', section_handler, defaults, name='sections-by-number'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/courses/(?P<cid>\d+)/sections/study-abroad/$', section_handler, defaults_study_abroad, name='sections-by-study-abroad'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/courses/(?P<cid>\d+)/sections/crn-(?P<crn>\d+)/$', section_handler, defaults, name='sections-by-crn'),
    # and departments
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/departments/$', dept_handler, defaults, name='departments'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/departments/(?P<code>[A-Za-z0-9]+)/$', dept_handler, defaults, name='department'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/departments/(?P<code>[A-Za-z0-9]+)/courses/$', bulk_course_handler, defaults, name='courses-by-department'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/departments/(?P<code>[A-Za-z0-9]+)/(?P<number>\d+)/$', course_handler, defaults, name='courses-by-number'),

    # periods, mostly for backbone
    url(r'^periods/$', period_handler, defaults, name='periods'),
    url(r'^periods/(?P<pid>\d+)/$', period_handler, defaults, name='period'),

    # computation APIs
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/schedules/', compute_schedule_handler, defaults, name='scheduler'),
    # the old API computed schedules on every request... quite slow!
    # the new one caches to the database to avoid repeated schedule computations
    #url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/old-schedules/', schedule_handler, defaults, name='scheduler'),
)
