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

git commit -m "
changed: use new variable: noisy_interferogram to calculate image quality metrics
problems: yaml functions are not working
implemented: 
    generate_dataset.py:
        - DatasetGenerator class: 
            - _extract_metrics (testing)
"