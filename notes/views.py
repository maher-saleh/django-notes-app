from django.shortcuts import render, get_object_or_404
from .models import Note
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from .forms import NotesForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/list.html'
    login_url = '/admin'
    
    def get_queryset(self):
        return self.request.user.notes.all()

@method_decorator(csrf_exempt, name='dispatch')
class PopularNotesListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/list.html'
    queryset = Note.objects.filter(likes__gte=1)
    login_url = '/admin'

@method_decorator(csrf_exempt, name='dispatch')
class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    context_object_name= 'note'
    template_name = 'notes/detail.html'
    login_url = '/admin'

@method_decorator(csrf_exempt, name='dispatch')
class NoteSharedView(DetailView):
    model = Note
    context_object_name= 'note'
    template_name = 'notes/detail.html'
    queryset = Note.objects.filter(is_public=True)

@method_decorator(csrf_exempt, name='dispatch')
class NotesCreateView(LoginRequiredMixin, CreateView):
    model = Note
    # fields = ('title', 'text')
    form_class = NotesForm
    template_name = 'notes/new.html'
    success_url = '/smart/notes'
    login_url = '/admin'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(csrf_exempt, name='dispatch')
class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    # fields = ('title', 'text')
    form_class = NotesForm
    template_name = 'notes/new.html'
    success_url = '/smart/notes'
    login_url = '/admin'

@method_decorator(csrf_exempt, name='dispatch')
class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/delete.html'
    success_url = '/smart/notes'
    login_url = '/admin'

@csrf_exempt
def NoteLikeView(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk)
        note.likes += 1
        note.save()
        return HttpResponseRedirect(reverse('notes.detail', args=(pk,)))
    raise Http404

@csrf_exempt
def NoteVisibilityView(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk)
        note.is_public = not note.is_public
        note.save()
        return HttpResponseRedirect(reverse('notes.detail', args=(pk,)))
    raise Http404
    

# def note_list(request):
#     notes = Note.objects.all()
#     return render(request, 'notes/list.html', {'notes': notes})

# def note_details(request, pk):
#     try:
#         note = Note.objects.get(pk=pk)
#     except Note.DoesNotExist:
#         raise Http404('Note doesn\'t exist')
#     return render(request, 'notes/detail.html', {'note': note})