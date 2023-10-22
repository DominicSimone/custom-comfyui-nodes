# custom-comfyui-nodes

Written for [ComfyUI](https://github.com/comfyanonymous/ComfyUI). See their [example node](https://github.com/comfyanonymous/ComfyUI/blob/master/custom_nodes/example_node.py.example) here. 



### Dynamic Text Node
Allows for more dynamic prompting using angle brackets. Nesting is supported. At the moment of writing this README I realize that surrounding whitespace is never stripped, keep that in mind as it may give unexpected results when assigning to names containing whitespace.

#### Unweighted choices
The random engine is seeded by an input to this node, so you can achieve consistent choices for the same image by passing in the same seed to both this node and the KSampler node.
```
<Mana|health|stamina> potion sitting on a <desk|table|bookshelf>.
-> can turn into ->
health potion sitting on a bookshelf
or
stamina potion sitting on a desk
```

#### Token Variable
Remember the same token choice from one template and use it later.
```
In <$season|summer|winter|fall|spring>, I cover my indoor office with <$season> patterned wallpaper.
-> can turn into ->
In summer, I cover my indoor office with summer patterned wallpaper.
or
In winter, I cover my indoor office with winter patterned wallpaper.
```

#### Positional Variable
Remember the same position that was chosen and use it later. Wraps around if the second template has fewer choices than the first.
```
My favorite fruit is <#name|apple|banana|coconut|dragonfruit>, so I want to try <#name|avocado|blueberry|cloudberry>.
-> can turn into ->
My favorite fruit is banana, so I want to try blueberry.
or
My favorite fruit is dragonfruit, so I want to try avocado.

```

#### Template from File
Collects templates from .json files located in custom_nodes/templates. A token like '.color' will be replaced by a random option if chosen. Does not support recursive templating.
```json
{
  "fruit": [
    "oranges",
    "bananas"
  ],
  "color": [
    "red",
    "blue"
  ]
}
```

```
A bowl full of <.fruit>. Sliced <$f|watermelon|.fruit> next to a whole <$f>
-> can turn into ->
A bowl full of oranges. Sliced banana next to a whole banana
```

#### Ignore Template
Omit this template from the final prompt.
```
Open window, <!steaming pie,|an orange juice,> open blinds 
->
Open window, open blinds
```

### Install Instructions
Place in the ComfyUI/custom_nodes folder and restart the service. Node will be available in the `utils` group.
