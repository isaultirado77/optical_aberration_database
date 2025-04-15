# TODO

- [ ] zernike polynomials.py
    - [X] implement functions
    - [ ] write doc
    - [ ] test

- [X] interferogram_generator.py 
    - [X] generate_interferogram (write doc)

- [ ] utils.py
    - [X] add_gaussian_noise
    - [X] add_poisson_noise
    - [X] add_dust
    - [X] vibration_blurr 

- [ ] metrics
    - [ ] image_quality.py
    - [ ] satistical.py
    - [ ] texture.py
    - [ ] zernike_metrics.py

- [ ] generate_dataset.py
    - [ ] configure for .yaml files for configuration
    - [ ] use tqdm to show progress (optional)

- [ ] generate_dataset.py
    - [X] generate_aberrations
    - [X] save_metadata
    - [X] generate_image_and_save
    - [X] add_vibration_blurr

- [ ] investigate licences and creative commons
- [ ] investigate multiprocessing for optimization of the dataset generation.  

git commit -m "Functions implemented: 
- metrics: {
    __init__.py: implemented
    statistical.py: calculate statistics, auxilars
    image_quality.py: calculate_pnsr, calculate_ssim
    texture.py: calculate_haralick_features

}

ready for testing
"

# https://www.scirp.org/journal/paperinformation?paperid=90911