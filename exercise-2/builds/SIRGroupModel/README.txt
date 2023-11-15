

For rebuilding the vadere software, you have to download the vadere master from github and replace the following files in corresponding locations.

The files SIRGroup.java, SIRGroupModel.java (updated version that's in git) and SIRType.java within folder “sir” should be moved into a newly created folder at the directory VadereSimulator/src/org/vadere/simulator/models/groups/sir;
AbstractGroupModel.java moved into VadereSimulator/src/org/vadere/simulator/models/groups;
AttributesSIRG.java moved into VadereState/src/org/vadere/state/attributes/models;
FootStepGroupIDProcessor.javamovedintoVadereSimulator/src/org/vadere/simulator/projects/dataprocessing/processor.

And also as the following files were updated (in source code), here is the updated file version, you just need to replace those in source code before building.
VadereGui/src/org/vadere/gui/components/model/SimulationModel.java
VadereSimulator/src/org/vadere/simulator/control/simulation/Simulation.java