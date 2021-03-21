from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from rest_framework.decorators import action, api_view
from ecs_backend.utility import exception_detail
from .controllers import CourseController

class CourseViewSet(viewsets.ModelViewSet, CourseController):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=False, methods=['POST'], url_path='data_upload')
    def data_upload(self, request):
        """
        METHOD : POST
        BODY TO SEND: {
            "file": <file in memory object>
        }
        RESPONSE (SUCCESS) : {
            "message": "Success in uploading course sheet ."
        }
        RESPONSE (ERROR) : {
            "message": "Error in course data upload . Please try Again"
        }
        :param request: request data containing the file object
        :return:
        """
        try:
            msg = self.course_sheet_upload(request)
            return Response(data={'message': msg},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            exception_detail(e)
            return Response(data={'message':'Error in course data upload . Please try Again'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['GET'], url_path='(?P<id>\d+)')
    def get(self, request, id):
        """
        METHOD : POST
        PARAMS TO SEND: {

        }
        RESPONSE (SUCCESS) : {
            "data": {
                "id": 801,
                "title": "The Art of Scala",
                "on_discount": false,
                "price": "20.0",
                "discount_price": "2.0",
                "description": "Scala is a multi-paradigm, general-purpose programming language.",
                "image_path": "",
                "date_created": "2021-03-21T13:00:29.232276Z",
                "date_updated": "2021-03-21T13:00:29.232276Z"
            }
        }
        RESPONSE (ERROR) : {
            "message": "Course 0 does not exist"
        }
        Get a course by id.
        :param int id: The record id.
        :return: A single course (see the challenge notes for examples)
        :rtype: object
        """
        """
        -------------------------------------------------------------------------
        Challenge notes:
        -------------------------------------------------------------------------
        1. Bonus points for not using a linear scan on your data structure.
        """
        try:
            data = self.get_course_data(request, id)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            exception_detail(e)
            return Response(data={'message': 'Course 0 does not exist'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['POST'])
    def post(self, request):
        """
        METHOD : POST
        BODY TO SEND: {
            "title" : "Brand new course",
            "image_path" : "images/some/path/foo.jpg",
            "price" : 25.0,
            "on_discount" : false,
            "discount_price" : 5.0,
            "description" : "This is a brand new course"
        }
        RESPONSE (SUCCESS) : {
            "id": 1001,
            "title": "Brand new course",
            "on_discount": false,
            "price": "25.0",
            "discount_price": "5.0",
            "description": "This is a brand new course",
            "image_path": "images/some/path/foo.jpg",
            "date_created": "2021-03-21T13:43:57.424628Z",
            "date_updated": "2021-03-21T13:43:57.424628Z"
        }
        RESPONSE (ERROR) : {
            "message": "Error in saving Course data."
        }
        Create a course.
        :return: The course object (see the challenge notes for examples)
        :rtype: object
        """

        """
        -------------------------------------------------------------------------
        Challenge notes:
        -------------------------------------------------------------------------
        1. Bonus points for validating the POST body fields
        """
        try:
            data = self.create_course_data(request)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            exception_detail(e)
            return Response(data={'message': 'Course 0 does not exist'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PUT'], url_path='(?P<id>\d+)')
    def put(self, request, id):
        """
        METHOD : POST
        BODY TO SEND: {
          "title": "Blah blah blah",
          "image_path": "images/some/path/foo.jpg",
          "price": 25.0,
          "on_discount": false,
          "discount_price": 5.0,
          "description": "New description",
          "id": 1001
        }
        RESPONSE (SUCCESS) : {
            "data": {
                "id": 1001,
                "title": "Blah blah blah",
                "on_discount": false,
                "price": "25.0",
                "discount_price": "5.0",
                "description": "New description",
                "image_path": "images/some/path/foo.jpg",
                "date_created": "2021-03-21T13:43:57.424628Z",
                "date_updated": "2021-03-21T13:51:03.134609Z"
            }
        }
        RESPONSE (ERROR) : {
            "message": "The id does match the payload."
        }
        Update a a course.
        :param int id: The record id.
        :return: The updated course object (see the challenge notes for examples)
        :rtype: object
        """

        """
        -------------------------------------------------------------------------
        Challenge notes:
        -------------------------------------------------------------------------
        1. Bonus points for validating the PUT body fields, including checking
           against the id in the URL

        """
        try:
            data = self.update_course_data(request, id)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            exception_detail(e)
            return Response(data={'message': 'Course 0 does not exist'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], url_path='(?P<id>\d+)')
    def delete(self, request, id):
        """
        METHOD : POST
        BODY TO SEND: {
        }
        RESPONSE (SUCCESS) : {
            "message": "The specified course was deleted"
        }
        RESPONSE (ERROR) : {
            "message": "Course 1005 does not exist"
        }
        Delete a course
        :return: A confirmation message (see the challenge notes for examples)
        """
        """
        -------------------------------------------------------------------------
        Challenge notes:
        -------------------------------------------------------------------------
        None
        """
        try:
            data = self.delete_course_data(request, id)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            exception_detail(e)
            return Response(data={'message': 'Course '+ id +' does not exist'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_courses(request):
    """
    METHOD : POST
    BODY TO SEND: {
        "page-number": page-number as number ,
        "page-size": page-size as size of data per page,
        "title-words": title-words search text
    }
    RESPONSE (SUCCESS) : {
        "data": [
            {
                "id": 830,
                "title": "The Best Way To Django",
                "on_discount": true,
                "price": "20.0",
                "discount_price": "2.0",
                "description": "Django, named after Belgian guitarist Jean Reinhardt, is a Python-based, free and open-source web framework.",
                "image_path": "",
                "date_created": "2021-03-21T13:00:29.233491Z",
                "date_updated": "2021-03-21T13:00:29.233491Z"
            },
            {
            ...
            }
        ]
    }
    RESPONSE (ERROR) : {
        "message": ""Course 0 does not exist""
    }
    Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    try:
        data = CourseController().get_course_page_list_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        exception_detail(e)
        return Response(data={'message': 'Course 0 does not exist'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

