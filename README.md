# custom-comfyui-nodes

Written for [ComfyUI](https://github.com/comfyanonymous/ComfyUI). See their [example node](https://github.com/comfyanonymous/ComfyUI/blob/master/custom_nodes/example_node.py.example) here. 



### Dynamic Text Node
Allows for more dynamic prompting using curly braces. Nesting is supported. At the moment of writing this README I realize that surrounding whitespace is never stripped, keep that in mind as it may give unexpected results when assigning to names containing whitespace.

#### Unweighted choices
The random engine is seeded by an input to this node, so you can achieve consistent choices for the same image by passing in the same seed to both this node and the KSampler node.
```
{Mana|health|stamina} potion sitting on a {desk|table|bookshelf}
->
health potion sitting on a bookshelf
```

#### Simple Variable
```
{$season|summer|winter|fall|spring} evening, indoor office with {$season} patterned wallpaper
->
summer evening, indoor office with summer patterned wallpaper
```

### Install Instructions
Place in the ComfyUI/custom_nodes folder and restart the service. Node will be available in the `utils` group.
