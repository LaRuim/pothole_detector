import os

images = [filename for root, dirs, files in os.walk("./test_set") for filename in files]
DEFAULT = "python label_image.py --graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt --input_layer=Placeholder --output_layer=final_result --image=./test_set/"

with open('run.sh', 'w') as r:
	for image in images:
		r.write(DEFAULT + image + '\n')
	


	
