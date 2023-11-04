package org.vadere.simulator.models.groups.sir;

import org.vadere.simulator.models.groups.Group;
import org.vadere.simulator.models.potential.fields.IPotentialFieldTarget;
import org.vadere.state.scenario.Pedestrian;
import org.vadere.state.scenario.ScenarioElement;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Stream;

public class SIRGroup implements Group {
	final private int id;
	final private int size;
	private  IPotentialFieldTarget potentialFieldTarget;
	final protected ArrayList<Pedestrian> members;

	public SIRGroup(int id,
				 SIRGroupModel model) {
		this.id = id;
		this.size = Integer.MAX_VALUE/2;
		this.potentialFieldTarget = model.getPotentialFieldTarget();
		members = new ArrayList<>();
	}

	@Override
	public int getID() {
		return id;
	}

	@Override
	public int hashCode() {
		return getID();
	}

	@Override
	public boolean equals(Group o) {
		boolean result = false;
		if (o == null){
			return result;
		}

		if (this == o) {
			result = true;
		} else {

			if (this.getID() == o.getID()) {
				result = true;
			}
		}

		return result;
	}

	@Override
	public List<Pedestrian> getMembers() {
		return members;
	}

	public Stream<Pedestrian> memberStream(){
		return members.stream();
	}

	@Override
	public int getSize() {
		return size;
	}

	@Override
	public boolean isMember(Pedestrian ped) {
		return members.contains(ped);
	}

	@Override
	public boolean isFull() {
		boolean result = true;

		if (members.size() < size) {
			result = false;
		}

		return result;
	}

	@Override
	public int getOpenPersons() {
		return size - members.size();
	}

	@Override
	public void addMember(Pedestrian ped) {
		members.add(ped);
	}

	@Override
	public boolean removeMember(Pedestrian ped){
		members.remove(ped);
		return (members.size() == 0);
	}

	@Override
	public void setPotentialFieldTarget(IPotentialFieldTarget potentialFieldTarget) {
		this.potentialFieldTarget = potentialFieldTarget;
	}

	@Override
	public IPotentialFieldTarget getPotentialFieldTarget() {
		return potentialFieldTarget;
	}

	@Override
	public void agentTargetsChanged(LinkedList<Integer> targetIds, int agentId) {

	}

	@Override
	public void agentNextTargetSet(double nextSpeed, int agentId) {

	}

	@Override
	public void agentElementEncountered(ScenarioElement element, int agentId) {

	}
}