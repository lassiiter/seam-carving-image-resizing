import numpy as np
import scipy as sp
import cv2

def get_grad_magnitude(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(float)
    x_grad = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    y_grad = cv2.Sobel(img, cv2.CV_64F, 0, 1)
    grad_mag_img = abs(x_grad) + abs(y_grad)

    return grad_mag_img

def get_backward_energy(img_orig):
    img = np.copy(img_orig)
    h,w = img.shape
    edge = 50
    for i in range(1,h):
        for j in range(w):
            if j == 0:
                img[i][j] = img[i][j] + min(img[i-1][j],img[i-1][j+1]) + edge
            elif j == w-1:
                img[i][j] = img[i][j] +  min(img[i-1][j],img[i-1][j-1])+ edge
            else:
                img[i][j] = img[i][j] + min(img[i-1][j-1],img[i-1][j],img[i-1][j+1])
    
    return img

def get_foward_energy(img_orig):
    img = np.copy(img_orig)
    h,w = img.shape
    energy_map = np.copy(img_orig)
    for i in range(h):
        for j in range(w):
            if j == 0:
                cost_mid = img[i-1][j] + abs(img[i][j]) + 20
                cost_right = img[i-1][j+1] + abs(img[i][j+1]-img[i][j]) + abs(img[i-1][j]-img[i][j+1])
                energy_map[i][j] = min(cost_mid,cost_right)
            elif j == w-1:
                cost_left = img[i-1][j-1] + abs(img[i][j]-img[i][j-1]) + abs(img[i-1][j]-img[i][j-1])
                cost_mid = img[i-1][j] + abs(img[i][j])
                energy_map[i][j] = min(cost_mid,cost_left)
            else:
                cost_left = img[i-1][j-1] + abs(img[i][j+1]-img[i][j-1]) + abs(img[i-1][j]-img[i][j-1])
                cost_mid = img[i-1][j] + abs(img[i][j+1]-img[i][j-1])
                cost_right = img[i-1][j+1] + abs(img[i][j+1]-img[i][j-1]) + abs(img[i-1][j]-img[i][j+1])
                energy_map[i][j] = min(cost_left,cost_mid,cost_right)
    
    return energy_map


def get_seam(img_orig):
    img = np.copy(img_orig)
    h,w = img.shape
    min_energy = min(img[h-1][:])
    s_idx = np.where(img[h-1][:] == min_energy)
    start_idx = s_idx[0][0]
    path = []
    path.append([h-1,start_idx])
    start_i = h-1
    start_j = start_idx
    for i in range(h-2,-1,-1):
        if start_j == 0:
            val = min(img[start_i-1][start_j],img[start_i-1][start_j+1])
        elif start_j == w-1:
            val = min(img[start_i-1][start_j],img[start_i-1][start_j-1])
        else:
            val = min(img[start_i-1][start_j],img[start_i-1][start_j-1],img[start_i-1][start_j+1])
        if val == img[start_i-1][start_j-1]:
            if start_j-1 < 0:
                path.append([start_i-1,start_j])
                start_j = start_j
                start_i = start_i-1
            else:
                path.append([start_i-1,start_j-1])
                start_j = start_j-1
                start_i = start_i-1
        elif val == img[start_i-1][start_j]:
            path.append([start_i-1,start_j])
            start_i = start_i-1
            start_j = start_j
        else:
            if start_j+1 < start_j:
                path.append([start_i-1,start_j])
                start_i = start_i-1
                start_j = start_j
            else:
                path.append([start_i-1,start_j+1])
                start_j = start_j+1
                start_i = start_i-1

    img_path = np.copy(img_orig)
    for p in path:
        img_path[p[0]][p[1]] = 1000000
    return path,img_path

def remove_seam_backward_energy(img_bw,img_color,num_seams):
    seams = []
    h,w,d = img_color.shape
    img_orig = np.copy(img_color)
    img_orig_idx = np.zeros((h,w), dtype=(tuple))
    for i in range(h):
        for j in range(w):
            img_orig_idx[i][j] = [i,j]

    for i in range(num_seams):
        h,w,d = img_color.shape
        grad_mag_img = get_grad_magnitude(img_color)
        img = get_backward_energy(grad_mag_img)
        seam,img_path = get_seam(img)
        seam.reverse()
        seam_idx = []
        for path in seam:
            seam_idx.append(img_orig_idx[path[0]][path[1]])
        seams.append(seam_idx)
        for i in range(h):
            for j in range(w-1):
                if j > seam[i][1]:
                    if j != w-1:
                        img_color[i][j-1] = img_color[i][j]
                        img_orig_idx[i][j-1] = img_orig_idx[i][j]
        img_color = img_color[:,:-1]
        img_orig_idx = img_orig_idx[:,:-1]
    return img_color,seams

def remove_seam_foward_energy(img_bw,img_color,num_seams):
    seams = []
    h,w,d = img_color.shape
    img_orig = np.copy(img_color)
    img_orig_idx = np.zeros((h,w), dtype=(tuple))
    for i in range(h):
        for j in range(w):
            img_orig_idx[i][j] = [i,j]
    for i in range(num_seams):
        h,w,d = img_color.shape
        grad_mag_img = get_grad_magnitude(img_color)
        energy_map = get_foward_energy(grad_mag_img)
        seam,img_seam = get_seam(energy_map)
        seam.reverse()
        seam_idx = []
        for path in seam:
            seam_idx.append(img_orig_idx[path[0]][path[1]])
        seams.append(seam_idx)
        for i in range(h):
            for j in range(w-1):
                if j > seam[i][1]:
                    if j != w-1:
                        img_color[i][j-1] = img_color[i][j]
                        img_orig_idx[i][j-1] = img_orig_idx[i][j]
        img_color = img_color[:,:-1]
        img_orig_idx = img_orig_idx[:,:-1]
    return img_color,seams

def draw_seams(seams,img):
    img_path = np.copy(img)
    h,w,d = img_path.shape
    seams.reverse()
    for seam in seams:
        for pair in seam:
            img_path[pair[0]][pair[1]] = [255,0,0]
    return img_path

def insert_seams(seams,img):
    img_bigger = np.copy(img)
    h,w,d = img_bigger.shape
    
    seam_num = -1
    for seam in seams:
        seam_num+=1
        img_bigger_old = np.copy(img_bigger)
        h,w,d = img_bigger_old.shape
        img_bigger = cv2.copyMakeBorder(img_bigger, 0 , 0 , 0 , 1 , cv2.BORDER_CONSTANT, None, 255).astype(float)
        h,w,d = img_bigger.shape
        for i in range(h):
            for j in range(w-1):
                if j >= seam[i][1]:
                    img_bigger[i][j+1] = img_bigger_old[i][j]
            img_bigger = img_bigger.astype(float)
            if seam[i][1] <= w-3:
                # Swap comment lines to draw inserted seams instead of creating real image
                img_bigger[seam[i][0]][seam[i][1]] = [255,0,0]
            else:
                # Swap comment lines to draw inserted seams instead of creating real image
                img_bigger[seam[i][0]][w-1] = [255,0,0]
        for seam_after in seams:
            if seams.index(seam_after) > seams.index(seam):
                for i in range(h):
                    if seam_after[i][1] > seam[i][1]:
                        seam_after[i][1] = seam_after[i][1] + 1
        img_bigger = img_bigger.astype(int)
        # print(seams)
    return img_bigger

def mean_standard_error(img1,img2):
    squared_diff = np.sum((img1 -img2) ** 2)
    num = img1.shape[0] * img1.shape[1]
    err = squared_diff / num
    return err

def cross_correlation(img1,img2):
    correlated = 0
    img1_flat = img1.flatten()
    img2_flat = img2.flatten()
    correlated = np.corrcoef(img1_flat,img2_flat,"full")
    coef = correlated[0,1]
    return coef
        
if __name__ == '__main__':
    img = cv2.imread('fig8_07_base.png')
    # Merge and split can be commented out when not using matplotlib to test results
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    img_bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(float)
    img_color = np.copy(img)
    img_orig = np.copy(img_color)

    img_color_backward,backward_seams = remove_seam_backward_energy(img_bw,img_color,50)
    img_path_backward = draw_seams(backward_seams,img_orig)
    expanded_images_backward = insert_seams(backward_seams,img_orig)

    # write file needs to be changed to write what file you actually want

    cv2.imwrite("fig9_08_backward_result.png.png", expanded_images_backward)



