import os
#Get Zone Descriptions
in_descr = open(os.path.join('..','ModelFiles', 'KZoneDescriptions.txt'), 'r')
zone_descr = in_descr.readlines()
zone_list = []
for item in zone_descr:
	list_val = item.split(' ')[0] + '-' + item.split(' ')[1]
	zone_list.append(list_val.strip('\n'))
    
print(zone_list)