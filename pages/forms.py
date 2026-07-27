from django import forms

from .models import MovieReview


class MovieReviewForm(forms.ModelForm):
	class Meta:
		model = MovieReview
		fields = ["rating", "review_text", "is_private"]
		widgets = {
			"rating": forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
			"review_text": forms.Textarea(attrs={"rows": 5, "placeholder": "Write your review"}),
		}
		labels = {
			"rating": "Rating (1-5)",
			"review_text": "Review",
			"is_private": "Make this review private",
		}