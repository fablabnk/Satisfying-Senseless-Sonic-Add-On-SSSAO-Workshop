# Alpha Petal

Displays a string on the SAO petal, one char at a time. the font is hand drawn and hard coded, crafted with love in the alley. The class needs to be initialized then can be passed a string consisting of [a-z] or space. There is no exception handling.


# Usage
### Initialization:
Initialize the class:
`ap = alpha_petal(petal_bus, PETAL_ADDRESS, time)`
### Displaying text
The `petal_string` function will not process uppercase. Any string passed will be displayed one letter at a time. spaces wipe and then wait to create temporal distance between words. I recommend ending with a space to delineate between iterations. 

    while True:
        pt.petal_string('alan supercon ')

