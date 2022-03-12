import os
import time
import cv2
import pybullet
import pybullet_data
from PIL import Image, ImageOps, ImageDraw, ImageFilter
from qibullet import SimulationManager
from qibullet import PepperVirtual

BACKGROUND_PATH = r'images/dorime.jpg'
SAMPLE_PATH = r'images/sample/'
TRANSFORMED_SAMPLE_PATH = r'images/transformedSample/'
SIZE = (128, 128)

textures = []

def transformImage(background, image):
    mirror = ImageOps.mirror(image)

    backgroundCopy = background.copy()
    backgroundCopy.paste(mirror, (400, 600))

    resizedImage = backgroundCopy.resize((200, 200))
    return resizedImage

def loadTextures(backgroundPath, samplePath):
    background = Image.open(backgroundPath)

    for root, dirs, files in os.walk(samplePath):
        for name in files:
            image = Image.open(os.path.join(root, name))
            transformedImage = transformImage(background, image)
            transformedImage.save(TRANSFORMED_SAMPLE_PATH + name)
            textures.append(pybullet.loadTexture(TRANSFORMED_SAMPLE_PATH + name))

def main():
    simulation_manager = SimulationManager()
    client = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())

    wall = pybullet.loadURDF("wall.urdf", basePosition=[4.0, 0.0, 1.0], useFixedBase=1, globalScaling=1.0, physicsClientId=client)

    loadTextures(BACKGROUND_PATH, SAMPLE_PATH) 

    handle = pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP) 

    for texture in textures:
        pybullet.changeVisualShape(objectUniqueId=wall, linkIndex=-1, textureUniqueId=texture)
        time.sleep(1)
        #Se obtiene lo que está viendo Pepper.
        image = pepper.getCameraFrame(handle)
        image = cv2.resize(image, SIZE, interpolation = cv2.INTER_AREA)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        cv2.imshow("top camera", image)
        #Se pone a la red a predecir.
        #se comunica el resultado.
        #Se presiona una tecla para avanzar a la siguiente imagen.
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
