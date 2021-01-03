from django.test import TestCase

# Create your tests here.
ImageFormSet = modelformset_factory(Image,
                                    form=ImageForm, extra=4)

if request.method == 'POST':
    ProductForm = ProductAddForm(request.POST)
    formset = ImageFormSet(request.POST, request.FILES,
                           queryset=ImageForm.objects.none())

    if ProductForm.is_valid() and formset.is_valid():

        ProductForm.save()

        for form in formset.cleaned_data:
            image = form['image']
            picture = ImageForm(product=ProductAddForm, image=image)
            picture.save()

        return HttpResponseRedirect('/vegetable/')
    else:
        print (ProductForm.errors, formset.errors)

else:
    VegetableForm = ProductAddForm()
    formset = ImageFormSet(queryset=Image.objects.none())

return render(request, 'vegetable/add.html',
              {'ProductForm': ProductForm, 'formset': formset},
              context_instance=RequestContext(request))