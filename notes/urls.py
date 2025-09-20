from django.urls import path
from . import views

urlpatterns = [
    path('notes', views.NotesListView.as_view(), name='notes.list'),
    path('notes/<int:pk>', views.NoteDetailView.as_view(), name='notes.detail'),
    path('notes/<int:pk>', views.NoteSharedView.as_view(), name='notes.detail'),
    path('notes/popular', views.PopularNotesListView.as_view()),
    path('notes/new', views.NotesCreateView.as_view(), name='notes.new'),
    path('notes/<int:pk>/edit', views.NoteUpdateView.as_view(), name='notes.update'),
    path('notes/<int:pk>/delete', views.NoteDeleteView.as_view(), name='notes.delete'),
    path('notes/<int:pk>/like', views.NoteLikeView, name='notes.like'),
    path('notes/<int:pk>/change_visibility', views.NoteVisibilityView, name='notes.change_visibility'),
    # path('notes', views.note_list),
    # path('notes/<int:pk>', views.note_details),
]
