from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True
    )  # Field to indicate if the domain is active or not
    is_default = models.BooleanField(
        default=False
    )  # Field to indicate if the domain is the default domain
    is_private = models.BooleanField(
        default=False
    )  # Field to indicate if the domain is private or restricted
    expiration_date = models.DateField(
        null=True, blank=True
    )  # Field to specify the expiration date of the domain
    is_verified = models.BooleanField(
        default=False
    )  # Field to indicate if the domain is verified or authenticated

    # Add more fields as needed for your specific requirements
    def __str__(self):
        return str(self.name)


class Subdomain(models.Model):
    name = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True
    )  # Field to indicate if the subdomain is active or not
    is_private = models.BooleanField(
        default=False
    )  # Field to indicate if the subdomain is private or restricted
    expiration_date = models.DateField(
        null=True, blank=True
    )  # Field to specify the expiration date of the subdomain
    is_verified = models.BooleanField(
        default=False
    )  # Field to indicate if the subdomain is verified or authenticated

    def get_full_domain(self):
        return self.name + "." + self.domain.name

    # Add more fields as needed for your specific requirements
    def __str__(self):
        return self.get_full_domain()
