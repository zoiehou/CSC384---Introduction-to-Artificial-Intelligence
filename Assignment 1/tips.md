/** WRITE YOUR TIPS IN THIS FILE **/

1. The use of deadlocks analysis helps a lot in terms of pruning states. Deadlocks are situations where the boxes will no longer be able to be moved
by the robots since they are stuck. 

2. Deadlocks can happen in a lot of situations, for example, when the boxes reach the edges of Sokoban board. They also can occur when boxes are stuck
between obstacles, so consider the edges and the obstacles.

3. When calculating Mahanttan distances, it is important to calculate not only the distances between robots to boxes, but also the distances between
boxes and storages. A good heuristic will tell the closest robot to push the closest box to the closest available storage as opposed to telling 
a far away robot to do so.
