##Version: 1.1
##Date: 21/Jun/2012

import Image, os, pyopencv

white = (255, 255, 255)

gpo_size_pos = {'111' : (450, 5), '112' : (450, 5), '311' : (450, 0), '511' : (450, 5),
                '512' : (450, 5), '221' : (430, 5), '211' : (465, 0), '811' : (485, 5)}

def change_photo_size(photo, new_photo, x_size, y_size):
    
    if os.path.lexists(photo):
        if os.path.getsize(photo) > 0:
            
            foto_orig = Image.open(photo)
            foto_mod = foto_orig.resize((x_size, y_size))
            foto_mod.save(new_photo, quality = 90)
            
            im = pyopencv.imread(new_photo)
            
            if pyopencv.imwrite(new_photo + '_new', im):
                os.remove(new_photo)
                os.rename(new_photo + '_new', new_photo)
            
            if os.path.lexists(new_photo):
                
                os.remove(photo)
            
            else:
                
                print 'Nao foi possivel modificar a foto.'
        
        else:
            print 'A foto esta vazia.'
    else:
        print 'A foto nao foi achada.'

def merge_photos(logo, photo, new_photo, x_size_photo, y_size_photo):
    
    if os.path.lexists(logo):
        cond_cont = True
    else:
        print 'O logo nao foi achado.'
        cond_cont = False
    
    if os.path.lexists(photo):
        cond_cont = True
    else:
        print 'A foto nao foi achada.'
        cond_cont = False
    
    if cond_cont:
    
        logo_code = logo[logo.rfind('\\') + 1: logo.rfind('.')]
        
        x_size_y_pos_logo = gpo_size_pos.get(logo_code)
        
        if x_size_y_pos_logo:
        
            x_size = x_size_y_pos_logo[0]
            y_pos_logo = x_size_y_pos_logo[1]
        
        else:
            
            x_size = 450
            y_pos_logo = 5
        
        x_pos_photo = x_size - x_size_photo    
        
        new_img = Image.new('RGB', [x_size, y_size_photo], white)
        
        logo_img = Image.open(logo, 'r')
        photo_img = Image.open(photo, 'r')
        
        new_img.paste(logo_img, (0, y_pos_logo))
        new_img.paste(photo_img, (x_pos_photo, 0))
        
        new_img.save(new_photo)
        
        if os.path.lexists(new_photo):
            os.remove(photo)
        else:
            print 'Nao foi possivel modificar a foto.'