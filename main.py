import timm
import urllib
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
import click
import torch

@click.command()
@click.option("--model", help="Number of greetings.")
@click.option("--image",  help="The person to greet.")
def hello(model, image):
    """Simple program that greets NAME for a total of COUNT times."""
    model = timm.create_model(model, pretrained=True) #
    model.eval()
    config = resolve_data_config({}, model=model)
    transform = create_transform(**config)

    url, filename = (image, "dog.jpg") #"https://github.com/pytorch/hub/raw/master/images/dog.jpg"
    urllib.request.urlretrieve(url, filename)
    img = Image.open(filename).convert('RGB')
    tensor = transform(img).unsqueeze(0) # transform and add batch dimension

    
    with torch.no_grad():
        out = model(tensor)
    probabilities = torch.nn.functional.softmax(out[0], dim=0)
    # print(probabilities.shape)
    # prints: torch.Size([1000])

    # Get imagenet class mappings
    url, filename = ("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", "imagenet_classes.txt")
    urllib.request.urlretrieve(url, filename) 
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]

    # Print top categories per image
    top5_prob, top5_catid = torch.topk(probabilities, 1)
    for i in range(top5_prob.size(0)):
        print({"predicted":categories[top5_catid[i]], "confidence":top5_prob[i].item()})

if __name__ == '__main__':
    hello()

