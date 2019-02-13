#Author-Jeffrey Krauss jeffreykrauss@live.com
#Description-Creates a stacked wavy bowl for laser cutting

import adsk.core, adsk.fusion, traceback
import math

defaultBowlName = 'WavyBowl'
defaultBaseDiameter = 5.08
defaultRingSize = 1.27
defaultMaterialThickness = 0.3175
defaultWaves = 12
defaultRings = 10
defaultAmplitudeStartPct = 25
defaultAmplitudeEndPct = 50
defaultRotationPct = 50
defaultCurve = 0

# global set of event handlers to keep them referenced for the duration of the command
handlers = []
app = adsk.core.Application.get()
if app:
    ui = app.userInterface

newComp = None

def createNewComponent():
    # Get the active design.
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component

class WavyBowlCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            unitsMgr = app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs

            bowl = WavyBowl()
            for input in inputs:
                if input.id == 'bowlName':
                    bowl.bowlName = input.value
                elif input.id == 'ringSize':
                    bowl.ringSize = unitsMgr.evaluateExpression(input.expression, "cm")
                elif input.id == 'baseDiameter':
                    bowl.baseDiameter = unitsMgr.evaluateExpression(input.expression, "cm")
                elif input.id == 'materialThickness':
                    bowl.materialThickness = unitsMgr.evaluateExpression(input.expression, "cm")
                elif input.id == 'waves':
                    bowl.waves = input.value
                elif input.id == 'rings':
                    bowl.rings = input.value
                elif input.id == 'amplitudePct':
                    bowl.amplitudeStartPct = input.valueOne
                    bowl.amplitudeEndPct = input.valueTwo
                elif input.id == 'renderFlat':
                    bowl.renderFlat = input.value
                elif input.id == 'curve':
                    bowl.curve = input.valueOne
                elif input.id == 'rotationPct':
                    bowl.rotationPct = input.valueOne

            bowl.buildWavyBowl()
            args.isValidResult = True

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class WavyBowlCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class WavyBowlCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):    
    def __init__(self):
        super().__init__()        
    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            onExecute = WavyBowlCommandExecuteHandler()
            cmd.execute.add(onExecute)
            onExecutePreview = WavyBowlCommandExecuteHandler()
            cmd.executePreview.add(onExecutePreview)
            onDestroy = WavyBowlCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            handlers.append(onExecutePreview)
            handlers.append(onDestroy)

            #define the inputs
            inputs = cmd.commandInputs
            inputs.addStringValueInput('bowlName', 'Bowl Name', defaultBowlName)

            initBaseDiameter = adsk.core.ValueInput.createByReal(defaultBaseDiameter)
            initRingSize = adsk.core.ValueInput.createByReal(defaultRingSize)
            initMaterialThickness = adsk.core.ValueInput.createByReal(defaultMaterialThickness)
            # Default sizes are presuming inches for measurements, make them nicer if using metric
            if app.activeProduct.unitsManager.defaultLengthUnits == 'mm' or app.activeProduct.unitsManager.defaultLengthUnits == 'm' or app.activeProduct.unitsManager.defaultLengthUnits == 'cm':
                initBaseDiameter = adsk.core.ValueInput.createByReal(5)
                initRingSize = adsk.core.ValueInput.createByReal(1)
                initMaterialThickness = adsk.core.ValueInput.createByReal(.3)
            else:
                initBaseDiameter = adsk.core.ValueInput.createByReal(defaultBaseDiameter)
                initRingSize = adsk.core.ValueInput.createByReal(defaultRingSize)
                initMaterialThickness = adsk.core.ValueInput.createByReal(defaultMaterialThickness)

            inputs.addValueInput('baseDiameter', 'Base Diameter', app.activeProduct.unitsManager.defaultLengthUnits, initBaseDiameter)

            inputs.addValueInput('ringSize', 'Ring Size', app.activeProduct.unitsManager.defaultLengthUnits, initRingSize)

            inputs.addValueInput('materialThickness', 'Material Thickness', app.activeProduct.unitsManager.defaultLengthUnits, initMaterialThickness)

            inputs.addIntegerSpinnerCommandInput('waves', 'Waves', 4, 100, 4, defaultWaves)

            inputs.addIntegerSpinnerCommandInput('rings', 'Rings', 1, 100, 1, defaultRings)

            slider = inputs.addIntegerSliderCommandInput('amplitudePct', 'Amplitude %', 0, 200, True)
            slider.valueOne = defaultAmplitudeStartPct
            slider.valueTwo = defaultAmplitudeEndPct

            slider = inputs.addIntegerSliderCommandInput('rotationPct', 'Rotation %', 1, 99)
            slider.valueOne = defaultRotationPct

            slider = inputs.addIntegerSliderCommandInput('curve', 'Curve', -75, 75)
            slider.valueOne = defaultCurve

            inputs.addBoolValueInput('renderFlat', 'Flatten', True)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class WavyBowl:
    def __init__(self):
        self._bowlName = defaultBowlName
        self._ringSize = defaultRingSize
        self._baseDiameter = defaultBaseDiameter
        self._materialThickness = defaultMaterialThickness
        self._waves = defaultWaves
        self._rings = defaultRings
        self._amplitudeStartPct = defaultAmplitudeStartPct
        self._amplitudeEndPct = defaultAmplitudeEndPct
        self._rotationPct = defaultRotationPct
        self._curve = defaultCurve
        self._renderFlat = False

    #properties
    @property
    def bowlName(self):
        return self._bowlName
    @bowlName.setter
    def bowlName(self, value):
        self._bowlName = value

    @property
    def ringSize(self):
        return self._ringSize
    @ringSize.setter
    def ringSize(self, value):
        self._ringSize = value

    @property
    def baseDiameter(self):
        return self._baseDiameter
    @baseDiameter.setter
    def baseDiameter(self, value):
        self._baseDiameter = value 

    @property
    def materialThickness(self):
        return self._materialThickness
    @materialThickness.setter
    def materialThickness(self, value):
        self._materialThickness = value 

    @property
    def waves(self):
        return self._waves
    @waves.setter
    def waves(self, value):
        self._waves = value   

    @property
    def rings(self):
        return self._rings
    @rings.setter
    def rings(self, value):
        self._rings = value  

    @property
    def amplitudeStartPct(self):
        return self._amplitudeStartPct
    @amplitudeStartPct.setter
    def amplitudeStartPct(self, value):
        self._amplitudeStartPct = value   

    @property
    def amplitudeEndPct(self):
        return self._amplitudeEndPct
    @amplitudeEndPct.setter
    def amplitudeEndPct(self, value):
        self._amplitudeEndPct = value  

    @property
    def rotationPct(self):
        return self._rotationPct
    @rotationPct.setter
    def rotationPct(self, value):
        self._rotationPct = value  

    @property
    def curve(self):
        return self._curve
    @curve.setter
    def curve(self, value):
        self._curve = value  

    @property
    def renderFlat(self):
        return self._renderFlat
    @renderFlat.setter
    def renderFlat(self, value):
        self._renderFlat = value  

    def buildWavyBowl(self):
        global newComp
        newComp = createNewComponent()
        if newComp is None:
            ui.messageBox('New component failed to create', 'New Component Failed')
            return

         # Create a new sketch.
        sketches = newComp.sketches
        xzPlane = newComp.xZConstructionPlane
        sketch = sketches.add(xzPlane)
        sketch.name = "Bowl"

        # Create curve 
        # No ability to do a circular pattern in a sketch so two options: draw entire circle or extrude a piece and do a circular pattern of the piece - going to go with the former for now
        # Design will be a sine wave centered on the current ring with the amplitude being calculated based on inputs
        # Should be able to do a spline with the points that are the top + bottom + middle of the wave
        # Math should be:
        #   x = (R + (a * sin(n * T))) * cos(T)
        #   y = (R + (a * sin(n * T))) * sin(T)
        # where
        #   R is circle's radius (ring diameter center distance)
        #   a is wave amplitude (half a ring size)
        #   T is the angle, from 0 to 2 * PI (step count will be 4 * waves - center, top, center, bottom)
        #   n is number of waves on circle

        amplitudeStep = (self._amplitudeEndPct - self.amplitudeStartPct) / self.rings
        steps = self.waves * 4
        thetaStep = 2 * math.pi / steps

        # Calculate the ring sizes for the bowl curve
        startingRingSize = self.ringSize * (self.curve + 100) / 100
        endingRingSize = (2 * self.ringSize) - startingRingSize
        ringSizeStep = (endingRingSize - startingRingSize) / self.rings

        radius = self.baseDiameter / 2

        for ring in range(0, self.rings + 1): # +1 since we need 2 circles to make 1 ring
            # Create an object collection for the points.
            points = adsk.core.ObjectCollection.create()

            # Define the points the spline with fit through.
            amplitude = self.ringSize * (self.amplitudeStartPct + (amplitudeStep * ring)) / 100
            diameter = 2 * (radius + amplitude)  # track the largest diameter we see

            # +1 to close the loop
            for step in range(0, steps + 1):
                theta = thetaStep * step
                x = (radius + (amplitude * math.sin(self.waves * theta))) * math.cos(theta)
                y = (radius + (amplitude * math.sin(self.waves * theta))) * math.sin(theta)
                points.add(adsk.core.Point3D.create(x, y, 0))

            # Create the spline.
            sketch.sketchCurves.sketchFittedSplines.add(points)

            # Increment the radius for the next ring
            radius += startingRingSize + (ring * ringSizeStep)

        newComp.name = self._bowlName + " (" + str("%.2f" % app.activeProduct.unitsManager.convert(diameter, "cm", app.activeProduct.unitsManager.defaultLengthUnits)) + " " + app.activeProduct.unitsManager.defaultLengthUnits +")"

        # "globals" for the extrusions
        extrudes = newComp.features.extrudeFeatures
        moveFeatures = newComp.features.moveFeatures
        distance = adsk.core.ValueInput.createByReal(self.materialThickness)
        distanceExtent = adsk.fusion.DistanceExtentDefinition.create(distance)
        bodiesForRotation = adsk.core.ObjectCollection.create()
        rotationStep = (2 * math.pi / self.waves) * self.rotationPct / 100
        rotationAmount = 0

        # Create base
        extrude = extrudes.addSimple(sketch.profiles[0], distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        bodyBase = extrude.bodies.item(0)
        bodyBase.name = "Base"

        # Create rings
        for ring in range(0, self.rings):
            # Extrude
            extrudeInput = extrudes.createInput(sketch.profiles[ring + 1], adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extrudeInput.setOneSideExtent(distanceExtent, adsk.fusion.ExtentDirections.PositiveExtentDirection) 
            if not self.renderFlat:
                extrudeInput.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(self.materialThickness * (ring + 1)))
            extrude = extrudes.add(extrudeInput)
            bodyRing = extrude.bodies.item(0)
            # Rotate the ring
            if not self.renderFlat:
                    rotationAmount += rotationStep
                    if not math.isclose(rotationAmount, (2 * math.pi)): # Fusion doesn't like a transform that has a rotation of 0 degrees
                        bodiesForRotation.add(bodyRing)
                        rotation = adsk.core.Matrix3D.create()
                        rotation.setToRotation(rotationAmount, adsk.core.Vector3D.create(0,1,0), adsk.core.Point3D.create(0,0,0))
                        moveFeatureInput = moveFeatures.createInput(bodiesForRotation, rotation)
                        moveFeatures.add(moveFeatureInput)
                        bodiesForRotation.clear()
            # Name the ring
            bodyRing.name = "Ring " + str(ring) 

def run(context):
    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('It is not supported in current workspace, please change to MODEL workspace and try again.')
            return
        commandDefinitions = ui.commandDefinitions
        # check if the command exists or not
        cmdDef = commandDefinitions.itemById('WavyBowl')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition('WavyBowl',
                    'Create a Wavy Bowl',
                    'Create a wavy bowl.')

        onCommandCreated = WavyBowlCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
