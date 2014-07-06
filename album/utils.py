'''
Created on 06-Jul-2014

@author: Rahul

@summary: Holds all the utility functions.
'''
import time
from datetime import datetime


def convert_datetime(datetime_str):
    '''
        Converts the datetime format: "Sat Jul 05 19:17:32 +0000 2014"
        into valid python datetime object.
    '''
    time_struct = time.strptime("Sat Jul 05 19:17:32 +0000 2014",
                                "%a %b %d %H:%M:%S +0000 %Y")
    return datetime(time_struct.tm_year, time_struct.tm_mon,
                    time_struct.tm_mday, time_struct.tm_hour,
                    time_struct.tm_min, time_struct.tm_sec)


def find_max_from_collection(objects, lookup_attr):
    '''
        Given the list of objects, finds the max value
        for lookup_attr.
    '''
    return max([getattr(obj, lookup_attr) for obj in objects])


def collection_to_map(objects, lookup_attr):
    '''
        Given the collection of objects, returns the mapping
        of lookup_attr:object.
        This can be used to remove duplicates from collection.
    '''
    uniq_objects = {}
    for obj in objects:
        uniq_objects.update({str(getattr(obj, lookup_attr)): obj})
    return uniq_objects
