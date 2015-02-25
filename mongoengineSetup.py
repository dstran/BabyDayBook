from mongoengine import *
# Will only import the Checkup class
from DataModel.Checkup import Checkup
# This will also import everything the file imports like mongoengine
# from DataModel.Checkup import *


connect('checkups_db2')

print Checkup.objects.count()

if Checkup.objects.count() == 0:
    Checkup.drop_collection()
    print Checkup.objects.count()

    newborn = Checkup(weight=91, weight_percent=0, height=18.9, height_percent=0, head_cir=0, head_cir_percent=0, notes='Newborn')
    newborn.save()
    oneMonth = Checkup(weight=134, weight_percent=26, height=21.75, height_percent=66, head_cir=14, head_cir_percent=17, notes='One month checkup')
    oneMonth.save()
    twoMonth = Checkup(weight=182, weight_percent=49, height=23.25, height_percent=68, head_cir=15, head_cir_percent=20, notes='Two month checkup')
    twoMonth.save()