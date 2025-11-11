from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Resource
from .forms import ResourceSubmissionForm


@login_required
def provider_dashboard(request):
    """Provider dashboard showing their resources."""
    resources = Resource.objects.filter(provider=request.user).order_by('-created_at')
    return render(request, 'provider/dashboard.html', {
        'resources': resources
    })


@login_required
def provider_resource_create(request):
    """Create a new resource submission."""
    if request.method == 'POST':
        form = ResourceSubmissionForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.provider = request.user
            resource.state = 'visible'
            resource.save()
            messages.success(request, 'Resource created successfully!')
            return redirect('resources:provider_dashboard')
    else:
        form = ResourceSubmissionForm()
    
    return render(request, 'provider/resource_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
def provider_resource_edit(request, pk):
    """Edit an existing resource."""
    resource = get_object_or_404(Resource, pk=pk, provider=request.user)
    
    # Check if editable
    if resource.state == 'rejected':
        messages.error(request, 'Cannot edit rejected resources.')
        return redirect('resources:provider_dashboard')
    
    if request.method == 'POST':
        form = ResourceSubmissionForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource updated successfully!')
            return redirect('resources:provider_dashboard')
    else:
        form = ResourceSubmissionForm(instance=resource)
    
    return render(request, 'provider/resource_form.html', {
        'form': form,
        'action': 'Edit',
        'resource': resource
    })


@login_required
def provider_resource_delete(request, pk):
    """Delete a resource."""
    resource = get_object_or_404(Resource, pk=pk, provider=request.user)
    
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted successfully!')
        return redirect('resources:provider_dashboard')
    
    return render(request, 'provider/resource_confirm_delete.html', {
        'resource': resource
    })
