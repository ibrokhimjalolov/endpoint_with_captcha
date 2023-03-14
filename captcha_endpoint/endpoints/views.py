from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import CaptchaRequired


class ProtectedView(APIView):

    permission_classes = (CaptchaRequired,)  # main security feature

    def get(self, request):
        self.do_expensive_computation()
        return Response({"message": "It works, congrats!"}, status=200)

    def do_expensive_computation(self):  # noqa
        # this is important and expensive action
        print("I'm doing something expensive here")


class NotProtectedView(APIView):

    def get(self, request):
        return Response({"message": "It works, congrats!"}, status=200)
