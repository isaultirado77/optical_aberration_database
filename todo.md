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
    - [X] image_quality.py
    - [X] satistical.py
    - [X] texture.py
    - [X] zernike_metrics.py

- [ ] generate_dataset.py
    - [X] configure for .yaml files for configuration
    - [X] use tqdm to show progress (optional)
    - [ ] use argparse for flexibility

- [ ] generate_dataset.py
    - [X] generate_aberrations
    - [X] save_metadata
    - [X] generate_image_and_save
    - [X] add_vibration_blurr

- [ ] investigate licences and creative commons
- [ ] investigate multiprocessing for optimization of the dataset generation.  

git commit -m "feat(blur): enhance motion blur and dataset prep

- Rewrite add_random_motion_blur() with:
  * Fixed kernel generation
  * Multi-channel support
- Normalize pure_aberrations syntax"
