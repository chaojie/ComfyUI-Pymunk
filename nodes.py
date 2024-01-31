import pymunk
import pygame
import json
import torch
import numpy as np
from PIL import Image, ImageFilter

class PymunkSpace:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "xgravity": ("FLOAT", {"default": 0}),
                "ygravity": ("FLOAT", {"default": 9.8}),
            }
        }
        
    RETURN_TYPES = ("PymunkSpace",)
    RETURN_NAMES = ("space",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,xgravity, ygravity):
        space = pymunk.Space()
        space.gravity = xgravity,ygravity
        return (space,)

class PygameSurface:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 576}),
                "height": ("INT", {"default": 320}),
            }
        }
        
    RETURN_TYPES = ("PygameSurface",)
    RETURN_NAMES = ("screen",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,width, height):
        pygame.init()
        size=(width,height)
        screen = pygame.Surface(size)
        #screen = screen.convert()
        #screen.fill((255, 255, 255))
        return (screen,)

class PymunkStaticLine:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "space": ("PymunkSpace",),
                "x1": ("FLOAT", {"default": 0}),
                "y1": ("FLOAT", {"default": 400}),
                "x2": ("FLOAT", {"default": 0}),
                "y2": ("FLOAT", {"default": 500}),
                "radius": ("FLOAT", {"default": 5}),
                "elasticity": ("FLOAT", {"default": 0.7}),
            },
            "optional": {
                "shape": ("SHAPE",{"default": None}),
            }
        }
        
    RETURN_TYPES = ("SHAPE",)
    RETURN_NAMES = ("line",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,space, x1,y1,x2,y2,radius,elasticity,shape=None):
        line_body=pymunk.Body(body_type=pymunk.Body.STATIC)
        line_shape=pymunk.Segment(line_body,(x1,y1),(x2,y2),radius)
        line_shape.elasticity=elasticity
        space.add(line_body,line_shape)
        return ([line_shape],)

class PymunkDynamicBox:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "space": ("PymunkSpace",),
                "x": ("FLOAT", {"default": 0}),
                "y": ("FLOAT", {"default": 0}),
                "width": ("FLOAT", {"default": 10}),
                "height": ("FLOAT", {"default": 10}),
                "radius": ("FLOAT", {"default": 1}),
                "mass": ("FLOAT", {"default": 1}),
                "elasticity": ("FLOAT", {"default": 1}),
            },
            "optional": {
                "shape": ("SHAPE",{"default": None}),
            }
        }
        
    RETURN_TYPES = ("SHAPE",)
    RETURN_NAMES = ("box",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,space,x,y, width,height,radius,mass,elasticity,shape=None):
        body = pymunk.Body()
        body.position = x,y

        poly = pymunk.Poly.create_box(body,(width,height),radius)
        poly.mass = mass    
        poly.elasticity = elasticity
        space.add(body, poly)       
        return ([poly],)


class PymunkDynamicCircle:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "space": ("PymunkSpace",),
                "x": ("FLOAT", {"default": 0}),
                "y": ("FLOAT", {"default": 0}),
                "radius": ("FLOAT", {"default": 1}),
                "mass": ("FLOAT", {"default": 1}),
                "elasticity": ("FLOAT", {"default": 1}),
            },
            "optional": {
                "shape": ("SHAPE",{"default": None}),
            }
        }
        
    RETURN_TYPES = ("SHAPE",)
    RETURN_NAMES = ("circle",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,space,x,y,radius,mass,elasticity,shape=None):
        body = pymunk.Body()
        body.position = x,y

        circle = pymunk.Circle(body,radius)
        circle.mass = mass         
        circle.elasticity=elasticity   
        space.add(body, circle)       
        return ([circle],)

class PymunkShapeMerge:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shape1": ("SHAPE",),
                "shape2": ("SHAPE",),
            },
        }
        
    RETURN_TYPES = ("SHAPE",)
    RETURN_NAMES = ("shape",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,shape1,shape2):     
        return (shape1+shape2,)

class PymunkRun:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "space": ("PymunkSpace",),
                "delta_t": ("FLOAT",{"default":0.02}),
                "frame_length": ("INT",{"default":14}),
                "width": ("INT", {"default": 576}),
                "height": ("INT", {"default": 320}),
                "shape": ("SHAPE",{"default": None}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tracking_points",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,space,delta_t,frame_length,width,height,shape):#, **kwargs
        tracking_points=[]
        for _ in range(frame_length):
            space.step(delta_t)
            i=0
            for obj in shape:
                if i>=len(tracking_points):
                    tracking_points.append([])
                _x=obj.body.position.x
                _y=obj.body.position.y
                if _x>width-1:
                    _x=width-1
                if _x<0:
                    _x=0
                if _y>height-1:
                    _y=height-1
                if _y<0:
                    _y=0
                tracking_points[i].append([_x,_y])
                i=i+1

        return (json.dumps(tracking_points),)

class PygameRun:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "screen": ("PygameSurface",),
                "space": ("PymunkSpace",),
                "delta_t": ("FLOAT",{"default":0.02}),
                "frame_length": ("INT",{"default":14}),
                "shape": ("SHAPE",{"default": None}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,screen,space,delta_t,frame_length,shape):#, **kwargs
        WHITE=(255,255,255)
        BLACK=(0,0,0)
        RED=(255,0,0)
        BLUE=(0,0,255)
        GREEN=(0,128,0)
        data=[]
        for _ in range(frame_length):
            space.step(delta_t)
            screen.fill(WHITE)
            i=0
            for obj in shape:
                if type(obj) is pymunk.shapes.Poly:
                    pygame.draw.polygon(screen, GREEN, obj.get_vertices())
                elif type(obj) is pymunk.shapes.Segment:
                    pygame.draw.line(screen, BLACK, obj.a,obj.b)
                elif type(obj) is pymunk.shapes.Circle:
                    pygame.draw.circle(screen,RED,(obj.body.position.x,obj.body.position.y),obj.radius)
                i=i+1
            
            pil_string_image = pygame.image.tostring(screen, "RGB", False)
            pli_image = Image.frombytes('RGB', screen.get_size(), pil_string_image, 'raw')
            data.append(pli_image)
        data = [torch.unsqueeze(torch.tensor(np.array(image).astype(np.float32) / 255.0), 0) for image in data]
        return torch.cat(tuple(data), dim=0).unsqueeze(0)


NODE_CLASS_MAPPINGS = {
    "PymunkSpace":PymunkSpace,
    "PygameSurface":PygameSurface,
    "PymunkRun":PymunkRun,
    "PygameRun":PygameRun,
    "PymunkStaticLine":PymunkStaticLine,
    "PymunkDynamicBox":PymunkDynamicBox,
    "PymunkDynamicCircle":PymunkDynamicCircle,
    "PymunkShapeMerge":PymunkShapeMerge,
}

