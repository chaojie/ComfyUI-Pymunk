import pymunk
import json

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
        return (line_shape,)

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
            },
            "optional": {
                "shape": ("SHAPE",{"default": None}),
            }
        }
        
    RETURN_TYPES = ("SHAPE",)
    RETURN_NAMES = ("box",)
    FUNCTION = "run"
    CATEGORY = "Pymunk"

    def run(self,space,x,y, width,height,radius,mass,shape=None):
        body = pymunk.Body()
        body.position = x,y

        poly = pymunk.Poly.create_box(body,(width,height),radius)
        poly.mass = mass              
        space.add(body, poly)       
        return ([poly],)

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
        '''
        for objects in kwargs.values():
            for obj in objects:
                obj_points=[]
                tracking_points.append(obj_points)
        for _ in range(frame_length):
            space.step(delta_t)
            i=0
            for objects in kwargs.values():
                for obj in objects:
                    tracking_points[i].append([obj.body.position.x,obj.body.position.y])
                    i=i+1
        '''

        return (json.dumps(tracking_points),)


NODE_CLASS_MAPPINGS = {
    "PymunkSpace":PymunkSpace,
    "PymunkRun":PymunkRun,
    "PymunkStaticLine":PymunkStaticLine,
    "PymunkDynamicBox":PymunkDynamicBox,
}

