from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from .models import Module, Program
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from .forms import ProgramForm, ModuleForm
from django.views.decorators.http import require_GET



@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
def admin_home(request):
    return render(request, 'admin_dashboard/admin_home.html')
#=============================================================================
@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class AdminModuleList(View):
    template_name = 'admin_dashboard/module_list.html'

    def get(self, request, *args, **kwargs):
        modules = Module.objects.all()
        return render(request, self.template_name, {'modules': modules})


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class AdminModuleDetail(View):
    template_name = 'admin_dashboard/module_detail.html'

    def get(self, request, module_id, *args, **kwargs):
        module = get_object_or_404(Module, pk=module_id)
        reviews = module.module_review.all()
        return render(request, self.template_name, {'module': module, 'reviews': reviews})


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
def program_detail(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    reviews = program.program_review.all()
    return render(request, 'admin_dashboard/program_detail.html', {'program': program, 'reviews': reviews})


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class AdminProgramList(View):
    template_name = 'admin_dashboard/program_list.html'

    def get(self, request, *args, **kwargs):
        programs = Program.objects.all()
        return render(request, self.template_name, {'programs': programs})


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class AdminProgramDetail(View):
    template_name = 'admin_dashboard/program_detail.html'

    def get(self, request, program_id, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_id)
        reviews = program.program_review.all()
        return render(request, self.template_name, {'program': program, 'reviews': reviews})
    


@require_GET
def search_modules(request):
    query = request.GET.get('query', '')
    if query:
        modules = Module.objects.filter(
            Q(module_code__icontains=query) |
            Q(module_name__icontains=query) 
        )
    else:
        modules = Module.objects.all()

    results = []
    for module in modules:
        module_data = {
            'id': module.id,
            'module_code': module.module_code,
            'module_name': module.module_name,
            'module_leader': module.module_leader,
            'completed': module.module_review.exists() and module.module_review.first().completed,
            'completed_by': module.module_review.first().completed_by if module.module_review.exists() else ''
        }
        results.append(module_data)

    return JsonResponse({'results': results})

@require_GET
def search_programs(request):
    query = request.GET.get('query', '')
    if query:
        programs = Program.objects.filter(
            Q(program_code__icontains=query) |
            Q(program_name__icontains=query)
        )
    else:
        programs = Program.objects.all()

    results = []
    for program in programs:
        program_data = {
            'id': program.id,
            'program_code': program.program_code,
            'program_name': program.program_name,
            'program_leader': program.program_leader,
            'completed': program.program_review.exists() and program.program_review.first().completed,
            'completed_by': program.program_review.first().completed_by if program.program_review.exists() else ''
        }
        results.append(program_data)

    return JsonResponse({'results': results})
#===========================Form-------===================================

@user_passes_test(lambda u: u.is_staff)
def program_create(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_program_list')
    else:
        form = ProgramForm()
    return render(request, 'admin_dashboard/program_create.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def module_create(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_module_list')
    else:
        form = ModuleForm()
    return render(request, 'admin_dashboard/module_create.html', {'form': form})