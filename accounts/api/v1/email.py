from .serializers import RegistraionSerializer


class EmailSending(generics.GenericAPIView):
    serializer_class = RegistraionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()

        uidb64 = urlsafe_base64_encode(smart_bytes(employee.id))
        token = default_token_generator.make_token(user=employee)
        email_body = (
            "Click on the link below to activate your account\nhttp://127.0.0.1:8000/"
            + uidb64
            + "/"
            + token
        )

        send_mail(
            "Activate your EmployeeDev Account",
            email_body,
            settings.EMAIL_HOST_USER,
            [employee.email],
            fail_silently=False,
        )

        return Response("email has sent")
