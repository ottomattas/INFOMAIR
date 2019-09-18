#[Part 1a: data and domain modelling](https://uu.blackboard.com/webapps/blackboard/content/listContentEditable.jsp?content_id=_3274643_1&course_id=_122545_1)
* We used 51 sessions (*from voip-0a45bc863d-20130325_200321 to voip-3b81cbb287-20130326_031000*) in the **dstc2_test** dataset to model the transition diagram.
* Python code was created based on the task description.

##Deliverables
The zip file holds both the transition diagram and the python program.
We delivered **Team18_1a_1.zip** with successful results, while **Team18_1a_2.zip** is improved after feedback was received. **Team18_1a_2.zip** was not delivered for review as this was done during the practice session locally on 17/09/2019.


#[Part 1b: text classification](https://uu.blackboard.com/webapps/blackboard/content/listContentEditable.jsp?content_id=_3274643_1&course_id=_122545_1)
* We used the dstc2_traindev dataset to create the baselines.
* Python code was created based on the task description.

##Baseline systems
1) We parsed all the acts and created files with the output to describe the turns in appropriately named files (e.g "1b/baseline_data/ack").
2) After we had the turns separated, we parsed all the transcriptions for creating the ruleset for every act (e.g "1b/baseline_data/ack.t").
3) We created the baseline rules manually in "1b/baseline_rules".

##Machine learning
WIP

##Evaluation
WIP

##Deliverables
WIP
