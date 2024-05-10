import os
from dotenv import load_dotenv
import requests
import time
from PIL import Image
import io

load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

stability_model = "sd3-turbo"

def transform_image(image_path) -> bytes:
    # Load the image
    img = Image.open(image_path)
    original_width, original_height = img.size
    
    # Define target sizes
    target_sizes = [(1024, 576), (576, 1024), (768, 768)]
    
    # Calculate the closest target size preserving aspect ratio
    def aspect_ratio(size):
        return size[0] / size[1]
    
    original_aspect_ratio = aspect_ratio((original_width, original_height))
    
    # Find the closest target size
    closest_size = min(target_sizes, key=lambda size: abs(aspect_ratio(size) - original_aspect_ratio))
    
    # Calculate new size preserving aspect ratio
    if original_aspect_ratio > aspect_ratio(closest_size):
        new_width = closest_size[0]
        new_height = round(new_width / original_aspect_ratio)
    else:
        new_height = closest_size[1]
        new_width = round(new_height * original_aspect_ratio)
    
    # Resize the image
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Create a new image with the target size
    new_img = Image.new("RGB", closest_size, (255, 255, 255))
    
    # Paste the resized image onto the new image
    paste_position = ((closest_size[0] - new_width) // 2, (closest_size[1] - new_height) // 2)
    new_img.paste(resized_img, paste_position)
    
    # Convert the image to bytes in a supported format (JPEG)
    img_byte_arr = io.BytesIO()
    new_img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

def remove_background(image: bytes, output_path: str) -> bytes:
    import requests

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/remove-background",
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "image/*"
        },
        files={
            "image": image
        },
        data={
            "output_format": "png"
        },
    )

    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
    
    return response.content

def get_inpainting_mask(image_bytes):
    """
    This function takes an image in bytes format, converts it to a PIL Image, and returns a mask for inpainting.
    The mask will be a black and white image where black pixels represent no inpainting strength and white pixels represent maximum inpainting strength.
    
    Args:
    image_bytes (bytes): The image in bytes format from which to extract the inpainting mask.
    
    Returns:
    bytes: A black and white image in bytes format representing the inpainting mask.
    """
    
    from PIL import Image
    import numpy as np
    import io
    
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert image to RGBA if not already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Extract alpha channel as a numpy array
    alpha_channel = np.array(image.getchannel('A'))
    
    # Create a mask where pixels are 255 (white) if transparent (alpha value is 0), otherwise 0 (black)
    mask = np.where(alpha_channel == 0, 255, 0).astype(np.uint8)
    
    # Convert numpy array back to PIL Image
    mask_image = Image.fromarray(mask, mode='L')
    
    # Convert PIL Image to bytes
    mask_bytes_io = io.BytesIO()
    mask_image.save(mask_bytes_io, format='PNG')
    mask_bytes = mask_bytes_io.getvalue()
    
    return mask_bytes

def inpaint_background(image: bytes, mask: bytes, background_image_prompt: str, output_path: str) -> None:
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/edit/inpaint",
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "image/*"
        },
        files={
            "image": image,
            "mask": mask,
        },
        data={
            "prompt": background_image_prompt,
            "output_format": "jpeg",
        },
    )

    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

def replace_background_with_prompt(image: bytes, prompt: str, output_path: str):

    image_wo_background = remove_background(
        image = image,
        output_path = output_path.replace('images', 'images_wo_background')
    )
    mask = get_inpainting_mask(image_wo_background)
    inpaint_background(
        image = image_wo_background,
        mask = mask,
        background_image_prompt = prompt,
        output_path = output_path
    )
    
    return f"Image with background replacement generation successful! Output Path: {output_path} Prompt: {prompt}"

def generate_text_to_image(prompt, output_path: str):

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "image/*"
        },
        files={
            "none": '',
            },
        data={
            "prompt": prompt,
            "mode": "text-to-image",
            "output_format": "jpeg",
            "style_preset": "anime",
            "model": stability_model
        },
    )
    
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

    return f"Text to Image generation successful! Output Path: {output_path} Prompt: {prompt}"

def generate_image_to_image(image: bytes, prompt: str, output_path: str):

    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "image/*"
        },
        files={
            "none": '',
            "image": image,
            },
        data={
            "prompt": prompt,
            "mode": "image-to-image",
            "strength": 0.7,
            "output_format": "jpeg",
            "style_preset": "anime",
            "model": stability_model
        },
    )
    
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

    return f"Image to Image generation successful! Output Path: {output_path} Prompt: {prompt}"

def generate_video_from_image(image: bytes, output_path: str) -> None:
    
    def generate_video_id(image: bytes) -> str:
        response = requests.post(
            f"https://api.stability.ai/v2beta/image-to-video",
            headers={
                "authorization": f"Bearer {STABILITY_API_KEY}",
            },
            files={
                "image": image # open(image_path, "rb")
            },
            data={
                "seed": 0,
                "cfg_scale": 1.8,
                "motion_bucket_id": 127
            },
        )
        generation_id = response.json().get('id')
        
        return generation_id
    
    def get_generated_video(generation_id, output_path):

        while True:
            response = requests.request(
                "GET",
                f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}",
                headers={
                    'accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
                    'authorization': f"Bearer {STABILITY_API_KEY}"
                },
            )
            
            if response.status_code == 202:
                print("Generation in-progress, try again in 10 seconds.")
                time.sleep(10)
                continue
            elif response.status_code == 200:
                print("Generation complete!")
                video = response.content
                with open(output_path, 'wb') as file:
                    file.write(video)
                break
            else:
                raise Exception(str(response.json()))
        
        return f"Video generation successful! Video ID: {generation_id}, Output Path: {output_path}"

    generation_id = generate_video_id(image)
    get_generated_video(generation_id, output_path)



# image_path = "./assets/images/shinichi1.jpeg"
# image = transform_image(image_path)
# image_wo_background = remove_background(
#     image = image,
#     output_path = "./output/images/_test2.png"
# )
# mask = get_inpainting_mask(image_wo_background)
# inpaint_background(
#     image = image_wo_background,
#     mask = mask,
#     background_image_prompt = "an epic buddhist temple, 4k, hdr render, anime",
#     output_path = "./output/images/_test5.jpeg"
# )
# replace_background_with_prompt(
#     image = image,
#     prompt = "an epic buddhist temple, 4k, hdr render, anime",
#     output_path = "./output/images/6.jpeg"
# )

# prompt = "Detective Conan looking into the camera in front of a volcano"
# output_path = "./output/images/1.jpeg"
# image = generate_image_to_image(image, prompt, output_path)
# prompt = "Aerial view of London at night, the city lights illuminate the scene."
# output_path = "./output/images/2.jpeg"
# image = generate_text_to_image(prompt, output_path)

# image_path = "./output/images/2.jpeg"
# image = transform_image(image_path)
# generate_video_from_image(
#     image = image,
#     output_path = "./output/videos/1.mp4"
#     )


# TODO: terrible results lol doesn't work
# image_path = "./assets/images/conan1.jpeg"
# image = transform_image(image_path)
# replace_background(
#     image = image,
#     background_image_prompt = "the inside of a church",
#     output_path = "./output/images/_test.jpeg"
# )
