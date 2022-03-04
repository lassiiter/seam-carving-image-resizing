# Content-Aware image resizing
![lake](https://user-images.githubusercontent.com/50963416/156672296-ed6f61ef-0f6f-4f75-8d6a-939f5b834d57.gif)  
 Example gif taken from https://github.com/andrewdcampbell/seam-carving  

## Introduction
The goal of this project is to perform content-aware image resizing for both reduction and expansion with seam carving operator. This allows image to be resized without losing or distorting meaningful content from scaling. The code in this repository and technique described below is an implementation of the algorithm presented in Avidan and Shamir (2007) and Avidan, Rubinstein, and Shamir (2008) algorithms.

  http://www.eng.tau.ac.il/~avidan/papers/vidret.pdf  
  https://www.merl.com/publications/docs/TR2008-064.pdf  
  
## Algorithm Overview
### Seam Removal
1. Calculate energy map:  
> Energy is calculated by sum the absolute value of the gradient in both x direction and y direction for all three channel (B, G, R). Energy map is a 2D image with the same dimension as input image.  

2. Build accumulated cost matrix using forward energy: 
> This step is implemented with dynamic programming. The value of each pixel is equal to its corresponding value in the energy map added to the minimum new neighbor energy introduced by removing one of its three top neighbors (top-left, top-center, and top-right)

3. Find and remove minimum seam from top to bottom edge:  
> Backtracking from the bottom to the top edge of the accumulated cost matrix to find the minimum seam. All the pixels in each row after the pixel to be removed are shifted over one column to the left if it has index greater than the minimum seam.  

4. Repeat step 1 - 3 until achieving targeting width  

## Seam Insertion
Seam insertion can be thought of as inversion of seam removal and inserts new artificial pixels/seams into the image. We first perform seam removal for n seams on a duplicated input image and record all the coordinates in the same order when removing. Then, we insert new seams to original input image in the same order at the recorded coordinates location. The inserted artificial pixel values are derived from an average of left and right neighbors.  

## Removal
![fig5_07_base](https://user-images.githubusercontent.com/50963416/156672949-f42c79bc-4a4c-4d3c-8651-d2162403e651.png)  
![fig5_07_seam_removal](https://user-images.githubusercontent.com/50963416/156672953-f400bf8e-20f7-43b0-9c7d-f44553beda5e.png)  

## Expansion
![fig8_07_base](https://user-images.githubusercontent.com/50963416/156673009-a600b42e-a28f-456a-8292-aacbe7b117e5.png)
![fig8c_07_seams](https://user-images.githubusercontent.com/50963416/156673012-3e9ce2e1-af15-46a0-9687-7b8946bc9b3a.png)
![fig8d_07_insert50](https://user-images.githubusercontent.com/50963416/156673013-445c9258-77ce-43a0-9bd6-7e813c520823.png)
