import json
import os

print("Which Epoch?")
ep = input()

#pred file = path to predicted output json files

pred_file = r"C:\Users\Christina\Documents\DIP\Week5_COCO_eval\pred_files\train_feature_concat\feature_val_review_epoch_{}_pred.json".format(ep)
base_folder = r"C:\Users\Christina\Documents\DIP\Week4\img\val"
#base_folder = path to validation images
#gt_file = "test_dict.json"

with open(r"C:\Users\Christina\Documents\DIP\Week 11\epoch{}.html".format(ep),"w") as f:
    f.write('<html>\n')
    f.write('\t <table style="width:90%">\n')
    f.write('\t<tr>\n')
    f.write('\t<th>Image</th><th>generated-review</th><th>gt</th>\n')
    f.write('</tr>\n')


    reviews = json.load(open(pred_file,"r"))
    #gt = json.load(open(gt_file,"r"))

    for review in reviews:
        image_file = review["image_id"] + ".jpg"
        impath = os.path.join(base_folder,image_file)
        #print(os.path.isfile(impath))
        f.write('\t\t<tr><td>')
        f.write('<img src ={} alt={} width="200">'.format(impath,image_file))
        f.write('</td><td> {}'.format( review["caption"]))
        #f.write('</td><td> {} ({})'.format(gt[review["image_id"]],review["image_id"]))
        f.write('</td></tr>\n')

    f.write('</table>\n')
    f.write('</html>')
