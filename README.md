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
>Hello
## Removal
![fig5_07_base](https://user-images.githubusercontent.com/50963416/156672949-f42c79bc-4a4c-4d3c-8651-d2162403e651.png)  
![fig5_07_seam_removal](https://user-images.githubusercontent.com/50963416/156672953-f400bf8e-20f7-43b0-9c7d-f44553beda5e.png)  

## Expansion
![fig8_07_base](https://user-images.githubusercontent.com/50963416/156673009-a600b42e-a28f-456a-8292-aacbe7b117e5.png)
![fig8c_07_seams](https://user-images.githubusercontent.com/50963416/156673012-3e9ce2e1-af15-46a0-9687-7b8946bc9b3a.png)
![fig8d_07_insert50](https://user-images.githubusercontent.com/50963416/156673013-445c9258-77ce-43a0-9bd6-7e813c520823.png)
