from django.urls import path
from module_review import views
from module_review import admin_view as vs

urlpatterns = [
    path('login/', vs.custom_login, name='login'),
    path('academic-years/', views.academic_year_list, name='academic-year-list'),
    path('/module/<str:module_code>/previous-review/', views.previous_year_module_reviews, name='previous_reviews'),
    
    path('module/', views.module_list, name='module'),
    path('module-detail/', views.module_detail, name='module-details'),
    path('module/<str:module_code>/review/', views.module_review_list, name='module-review'),
    path('module-detail/review/<int:pk>/', views.module_review_detail, name='review-module-details'),
    path('module/review/<int:pk>/', views.module_review_detail, name='module-review-detail'),
    
    # ================PROGRAM================================================================
    path('program/', views.program_list, name='program'),
    path('program-detail/', views.program_detail, name='program-details'),

    path('program/<str:program_code>/review/', views.program_review_list, name='program-review'),
    path('program-detail/review/<int:pk>/', views.program_review_detail, name='review-program-details'),

    path('program/review/<int:pk>/', views.program_review_detail, name='program-review-detail'),
    
    #===========================Admin ===================================================
    path('admin/module/upload-xlsx/', views.module_upload_xlsx, name='admin_module_upload_xlsx'),
    path('admin/program/upload-xlsx/', views.program_upload_xlsx, name='admin_program_upload_xlsx'),
    path('admin/export_module_details/<int:module_id>/', views.export_module_details, name='export_module_details'),
    path('admin/export_module_details/<int:module_id>/<str:academic_year>/', views.export_ay_module_details, name='export_ay_module_details'),
    path('admin/export_program_details/<int:program_id>/', views.export_program_details, name='export_program_details'),
    path('admin/export_program_details/<int:program_id>/<str:academic_year>/', views.export_ay_program_details, name='export_ay_program_details'),
    path('admin/', vs.admin_home, name='home'),
    path('admin/modules/', vs.AdminModuleList.as_view(), name='admin_module_list'),
    path('admin/module/<int:module_id>/', vs.AdminModuleDetail.as_view(), name='admin_module_detail'),
    path('admin/programs/', vs.AdminProgramList.as_view(), name='admin_program_list'),
    path('admin/program/<int:program_id>/', vs.AdminProgramDetail.as_view(), name='admin_program_detail'),
    path('admin/search_modules/', vs.search_modules, name='search_modules'),
    path('admin/filter_modules/', vs.filter_modules, name='filter_modules'),
    path('admin/search_programs/', vs.search_programs, name='search_programs'),
    path('admin/filter_programs/', vs.filter_programs, name='filter_programs'),
    path('admin/module/add-module', vs.add_module, name='add_module'),
    path('admin/program/add-program', vs.add_program, name='add_program'),
    path('admin/program/create/', vs.program_create, name='admin_program_create'),
    path('admin/module/create/', vs.module_create, name='admin_module_create'),
    path('admin/academic-year/', vs.AdminAcademicYearList.as_view(), name='admin_academicyear_list'),
    path('admin/academic-year/add/', vs.add_academic_year, name='add_academic_year'),
    path('admin/academic-year/toggle-eval-accepting/<int:pk>/', vs.toggle_eval_accepting, name='toggle_eval_accepting'),

]
