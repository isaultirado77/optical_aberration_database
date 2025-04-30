# TODO

- [ ] implement multithreading for dataset generation
- [X] implement preprocess_data script

- [X] zernike polynomials.py
    - [X] implement functions
    - [X] write doc
    - [X] test

- [X] interferogram_generator.py 
    - [X] generate_interferogram (write doc)

- [X] utils.py
    - [X] add_gaussian_noise
    - [X] add_poisson_noise
    - [X] add_dust
    - [X] vibration_blurr 

- [X] metrics
    - [X] image_quality.py
    - [X] satistical.py
    - [X] texture.py
    - [X] zernike_metrics.py

- [X] generate_dataset.py
    - [X] configure for .yaml files for configuration
    - [X] use tqdm to show progress (optional)
    - [ ] use argparse for flexibility
    - [ ] use multithreading

- [X] generate_dataset.py
    - [X] generate_aberrations
    - [X] save_metadata
    - [X] generate_image_and_save
    - [X] add_vibration_blurr

- [X] investigate licences and creative commons
- [ ] investigate multiprocessing for optimization of the dataset generation.  

git commit -m "
version 1.0 ready:
implemented: visualization/animation scripts for generation 
of plots and gifs used in documentation 
- [ ] docs
    - [ ] metrics_details
    - [X] zernike_modes_reference
    - [X] visualization
    - [X] need to check typos; 
"