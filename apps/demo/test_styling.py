#########################################################################
##################### Dash Styling Example Document ##################### 
#########################################################################


import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

#Dictionary of Styling elements for Dash applications inline
#Note, its possible to combine elements into shorthand - for example, specify background properties 'background': '#ffffff url("img_tree.png") no-repeat right top';
#Note, in some cases, the pix values can be changed to be percent or cm or another unit
#Note, https://www.w3schools.com/css/ has a great deal of resources on CSS styling - below are just some of the key points

style = {'textAlign': 'left',
         'fontFamily': 'verdana',
         'fontSize': '20px',
         'color': '#0B3D6D',                        #Set the font colour
         'border': '2px',                           #Set the Border Width
         'backgroundColor' : '#FFFFFF',             #Set the background colour
         'opacity': '0.3',                          #Set the Opacity of an Element
         'backgroundImage:' : 'url',                #Set a background image from a URL
         'backgroundRepeat': 'no-repeat',           #Set the background image to not repeat
         'backgroundPosition': 'right top',         #set the background image position
         'backgroundAttachment': 'fixed',           #Determines if the background image should scroll or remain in place  
         'borderStyle':'none',                      #Set the border style, options include (dotted, dashed, solid, double, groove, ridge, inset, outset, none, hidden      
         'borderWidth': '5px 20px',                 #Set the border width 5px top and bottom, 20px on the sides
         'borderColor': 'red green blue yellow',    #red top, green right, blue bottom and yellow left
         'borderRadius': '5px',                     #Set the Border Radius
         'margin' : '5px',                          #Set margin to Auto, length,%, inherit and can also be specified for top, bottom, right, left
         'padding' : '5px',                         #Set the amount of whitespace around an elements content can also be specified for top, left, etc.
         'width': '5px',                            #Set width of the element's content area
         'height': '5px',                           #Set height of the element's content area
         'maxWidth': 'none',                        #Sets the maximum width of an element
         'columnCount': '2'                         #Specify the number of columns
        },

#an example of a layout using Dash Bootstrap https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div("A single, half-width column"),
                width={"size": 6, "offset": 3},
                style={'borderStyle': 'solid',
                       'borderWidth': '1px',
                       'borderColor': 'white',
                       'borderRadius': '5px'
                       }
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div("The last of three columns"),
                    width={"size": 3, "order": "last", "offset": 1},
                    style={'borderStyle': 'solid',
                           'borderWidth': '1px',
                           'borderColor': 'white',
                           'borderRadius': '5px'
                           }
                ),
                dbc.Col(
                    html.Div("The first of three columns"),
                    width={"size": 3, "order": 1, "offset": 2},
                    style={'borderStyle': 'solid',
                           'borderWidth': '1px',
                           'borderColor': 'white',
                           'borderRadius': '5px'
                           }
                ),
                dbc.Col(
                    html.Div("The second of three columns"),
                    width={"size": 3, "order": 12},
                    style={'borderStyle': 'solid',
                           'borderWidth': '1px',
                           'borderColor': 'white',
                           'borderRadius': '5px'
                           }
                ),
            ]
        ),
    ],
    style= {'borderStyle':'solid',
            'borderWidth': '2px',
            'borderColor': 'blue'
            }
)