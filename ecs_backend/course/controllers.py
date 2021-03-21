from .models import *
from ecs_backend.utility import *
from .serializers import *
import json
from django.db.models import Q
from django.core.paginator import Paginator

class CourseController():

    def course_sheet_upload(self, request):
        """
        function to upload the code sheet data and save into the database
        1. Get the data and then iterate over it and make objects of it for saving.
        2. append that into the crate_list
        3. using bulk_create , save the data into the database in one shot .
        :param request:
        :return:
        """
        msg = 'Error in course data upload . Please try Again'
        try:
            file_data = request.FILES.get('file')
            file_data = json.load(file_data)
            create_list = []
            for f_data in file_data:
                obj = Course()
                obj.title = f_data.get('title')
                obj.on_discount = f_data.get('on_discount', False)
                obj.price = f_data.get('price')
                obj.discount_price = f_data.get('discount_price')
                obj.description = f_data.get('description')
                obj.image_path = f_data.get('image_path')
                obj.date_created = f_data.get('date_created')
                obj.date_updated = f_data.get('date_updated')
                create_list.append(obj)
            Course.objects.bulk_create(create_list)
            msg = 'Success in uploading course sheet .'
        except Exception as e:
            exception_detail(e)
        return msg


    def get_course_data(self, request, course_id):
        """
        function to get the data according to the id , here by default there is indexing on id so fetching is not
        a linear search
        1. Querying the database and getting the particular data .
        2. Using serializer , serializing it and sending it
        :param request:
        :param course_id:
        :return:
        """
        data = {'message': 'Course ' + course_id + ' does not exist'}
        try:
            obj = Course.objects.get(id=course_id)
            serializer = CourseSerializer(obj)
            course_data = serializer.data
            data = {'data': course_data}
        except Exception as e:
            print('')
            exception_detail(e)
        return data


    def get_course_page_list_data(self, request):
        """
        function to the list of data to send again back with paginator ( Pagination )
        1. first getting the data needed from params, if not then setting default values as well , so it will work
            properly
        2. making a dynamic query filter with or condition for searching multiple text at once in single query
        3. after gettinge the Database obejct passing it to the paginator object.
        4. using that paginator object getting the exact page needed to send.
        5. serializing it and then sending the data in proper format
        :param request:
        :param course_id:
        :return:
        """
        data = {'message': 'Course 0 does not exist'}
        try:
            title_words = request.GET.get('title-words')
            page_size = request.GET.get('page-size', 10)
            page_number = request.GET.get('page-number', 1)
            title_filter = Q()
            if title_words:
                for title in title_words.split(','):
                    title_filter.add(Q(title__icontains=title), Q.OR)
            course_obj = Course.objects.filter(title_filter).order_by('id')
            paginator_obj = Paginator(course_obj, page_size)
            page_obj = paginator_obj.page(page_number)
            course_page_obj =page_obj.object_list
            course_serializer = CourseSerializer(course_page_obj, many=True)
            course_data = course_serializer.data
            data = {'data': course_data}
        except Exception as e:
            exception_detail(e)
        return data

    def create_course_data(self, request):
        """
        function to create the course using the data get into the body of teh rqeuest.
        1. first getting the data from the post request
        2. calling a fucntion for validation of the data provided
        3. making a blank course object and then sending it to function for creating the data into Database
        :param request:
        :param course_id:
        :return:
        """
        data = {'message': 'Error in saving Course data.'}
        try:
            post_data = request.data
            if post_data:
                success, msg = self.validate_course_fields_data(post_data)
                if success:
                    obj = Course()
                    success, course_data = self.create_or_update_course_data(obj, post_data)
                    if success:
                        data = {'data': course_data}
                else:
                    data = {'message': msg}
        except Exception as e:
            exception_detail(e)
        return data


    def validate_course_fields_data(self, post_data):
        """
        function to validate the data coming from request .
        1. checking for the values is present or not for on_discount, price, title, discount_price
        2. if they are not there then appending to the list
        3. using the above list making the error message
        :param post_data:
        :return:
        """
        success = False
        msg = 'Please provide the value for field : '
        field_list = []
        try:
            if not post_data.get('on_discount') in [True, False]:
                field_list.append('on_discount')
            if not post_data.get('price'):
                field_list.append('price')
            if not post_data.get('title'):
                field_list.append('title')
            if not post_data.get('discount_price'):
                field_list.append('discount_price')
            if field_list:
                msg += ','.join(field_list)
            else:
                success = True
        except Exception as e:
            exception_detail(e)
        return success, msg


    def update_course_data(self, request, course_id):
        """
        function to update the specidic data in the database record
        1. getting the data from the PUT rqeuest
        2. checking for the id is same or not
        3. if same then calling a fucntion for validation the data .
        4. getting the particular id object from the database and then sending it to function for updating the data .
        5. getting the serialize data and then sending it back.
        :param request:
        :param course_id:
        :return:
        """
        data = {'message': 'The id does match the payload.'}
        try:
            put_data = request.data
            if put_data and put_data.get('id') == int(course_id):
                success, msg = self.validate_course_fields_data(put_data)
                if success:
                    obj = Course.objects.get(id=course_id)
                    success, course_data = self.create_or_update_course_data(obj, put_data)
                    if success:
                        data = {'data': course_data}
        except Exception as e:
            exception_detail(e)
        return data


    def create_or_update_course_data(self, obj, request_data):
        """
        function to create or update the course data in database .
        1. first seeting the values into the object given in parameters
        2. saving it and then serialize the data and sending backa again.
        :param obj: create or update object
        :param request_data: data which need to update in the specific object
        :return:
        """
        success = False
        course_data = {}
        try:
            obj.title = request_data.get('title')
            obj.on_discount = request_data.get('on_discount')
            obj.price = request_data.get('price')
            obj.discount_price = request_data.get('discount_price')
            obj.description = request_data.get('description')
            obj.image_path = request_data.get('image_path')
            obj.save()
            course_serializer = CourseSerializer(obj)
            course_data = course_serializer.data
            success = True
        except Exception as e:
            exception_detail(e)
        return success, course_data


    def delete_course_data(self, request, course_id):
        """
        function to delete the specific record from the course data.
        1. getting the data from the database and them deleting it if it exists
        :param request:
        :param course_id:
        :return:
        """
        data = {'message': 'Course ' + course_id + ' does not exist'}
        try:
            Course.objects.get(id=course_id).delete()
            data = {'mesage': 'The specified course was deleted'}
        except Exception as e:
            exception_detail(e)
        return data

