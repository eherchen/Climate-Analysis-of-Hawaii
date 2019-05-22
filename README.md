# Homework-08-Submission

Step 1 - Climate Analysis and Exploration
Jupyter notebook 
Prcp vs date png
Station vs temp png

Step 2 - Climate App
app.py  

Notes: I had some ideas on the following, but could not get it to run like I had wanted it to.
* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
