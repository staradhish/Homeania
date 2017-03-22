from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()

class UserLoginForm(forms.Form):
	email = forms.EmailField(label='Email')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		# the_user = authenticate(email=email, password=password)
		# if not the_user:
		# 	raise forms.ValidationError('Invalid Credentials')
		
		user_obj = User.objects.filter(email=email).first()
		if not user_obj:
			raise forms.ValidationError('Invalid Email')
		else:
			if not user_obj.check_password(password):		
				raise forms.ValidationError('Invalid Password')
			if not user_obj.is_active:
				raise forms.ValidationError('Inactive User: Please verify email address!')
		self.cleaned_data['user_obj'] = user_obj
		return super(UserLoginForm, self).clean(*args, **kwargs)


	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
	# 	user_qs = User.objects.filter(email=email)
	# 	user_exists = user_qs.exists()
	# 	if not user_exists and user_qs.count() != 1:
	# 		raise forms.ValidationError('Invalid Credentials')
	# 	return email


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name','date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','date_of_birth','joining_date', 'level_id')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff')}),
    )
    readonly_fields = ['joining_date']
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



def take_quiz(level):
    # user_level = request.user.level_id
    # level = Level.objects.filter(id = user_level)
    for question in level:
        questions = question.question_set.all()
        for answer in questions:
            field_name = "question_%d" %question.id
            choices = []
            for a in answer.answer_set.all():
                 choices.append((a.id, a.answer_content,))
            print choices
    #return HttpResponseRedirect("/login")

    return type('TakeQuizForm', (forms.BaseForm,), {'base_fields': fields})


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)