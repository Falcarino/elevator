# Elevator (outdated description, will re-write)
The original task is taken from [here](https://www.codewars.com/kata/58905bfa1decb981da00009e)
## Short description
The program simulates an elevator in a building with fixed queues of people who want to go on different floors. The elevator and queues follow a specific set of rules:  
### Elevator rules
* The elevator always starts from the ground floor
* Each floor, aside from the top and ground ones, have **'Up'** and **'Down'** buttons.
* When the elevator is empty, it tries to find the most 'effecient' floor to stop at
    - While going **up** it's trying to find the highest floor at which someone wants to get to a lower floor
    - While going **down** it's trying to find the lowest floor at which someone wants to get to a higher floor
* The elevator never changes direction until there are no more people wanting to get on/off in the direction it is already travelling
* The elevator has, surprisingly, a finite amount of space, i.e. it can carry only a certain given amount of people at once
* The elevator will stop at the floor where it was called even if it is full and no one needs to get off
* When both the elevator and building are empty, the elevator returns back to the ground floor
### People behaviour
* Each floor has a queue (an empty queue is still technically a queue)
* Any person may press **'Up'** or **'Down'** buttons regardless of their position in the queue
* Only people going the same direction as the elevator is headed may enter it
* Entry is according to the "queue" order, although those unable to enter do not block those who can
## An example layout
```
Elevator's capacity: 3
        Initial setup                 Result                  
      /----------------\        /----------------\
    10|                |      10|                |
      |----------------|        |----------------|
     9| 1              |       9|                |
      |----------------|        |----------------|
     8|                |       8|                |
      |----------------|        |----------------|
     7| 1,1            |       7|                |
      |----------------|        |----------------|
     6|                |       6|                |
      |----------------|        |----------------|
     5|                |       5|                |
      |----------------|        |----------------|
     4| 0              |       4|              4 |
      |----------------|        |----------------|
     3|                |       3|                |
      |----------------|        |----------------|
     2| 4              |       2|              2 |
      |----------------|        |----------------|
     1| 2              |       1|          1,1,1 |
      |----------------|        |----------------|
     G|                |       G|              0 |
      |==========================================|

The elevator's steps:
-- go up --
'0' - starting point
'1' - picks up '2'
'2' - let '2' out and picks '4' up
'4' - let '4' out
-- go down --
'9' - pick up '1'
'7' - pick up '1' and '1'
'4' - the elevator is full, can't pick up '4'
'1' - let '1', '1' and '1' out
-- go up --
-- go down --
'4' - pick up '0'
'0' - let '0' out and endpoint
END
```

