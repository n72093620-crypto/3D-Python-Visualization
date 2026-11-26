import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="3D Bubble Sort",
    layout="wide"
)

st.title("3D Bubble Sort Visualization")
st.write("Watch numbers move step by step in 3D!")

numbers = [8, 3, 6, 2, 9, 1, 5, 4]

def make_trace(arr, active):
    traces = []

    for i, value in enumerate(arr):
        color = "orange" if i in active else "royalblue"

        traces.append(
            go.Scatter3d(
                x=[i, i],
                y=[0, 0],
                z=[0, value],
                mode="lines+markers+text",
                line=dict(color=color, width=18),
                marker=dict(size=4, color=color),
                text=["", str(value)],
                textposition="top center",
                name=f"Number {value}",
                showlegend=False
            )
        )

    return traces


states = [(numbers.copy(), [])]
arr = numbers.copy()

for i in range(len(arr)):
    for j in range(len(arr)-i-1):
        active = [j, j+1]

        if arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1], arr[j]

        states.append((arr.copy(), active))

fig = go.Figure(
    data=make_trace(states[0][0], states[0][1])
)

frames = []

for k, (values, active) in enumerate(states):
    frames.append(
        go.Frame(
            data=make_trace(values, active),
            traces=list(range(len(numbers))),
            name=str(k)
        )
    )

fig.frames = frames

fig.update_layout(
    title="3D Animated Bubble Sort",
    scene=dict(
        xaxis_title="Array Index",
        yaxis_title="Depth",
        zaxis_title="Number Value",
        aspectmode="manual",
        aspectratio=dict(x=2, y=1, z=1.5)
    ),
    updatemenus=[dict(
        type="buttons",
        buttons=[
            dict(
                label="Start Animation",
                method="animate",
                args=[None, {
                    "frame": {"duration": 500, "redraw": True},
                    "fromcurrent": True
                }]
            ),
            dict(
                label="Pause",
                method="animate",
                args=[[None], {
                    "frame": {"duration": 0, "redraw": False},
                    "mode": "immediate"
                }]
            )
        ]
    )],
    sliders=[dict(
        steps=[
            dict(
                method="animate",
                args=[[str(k)], {
                    "mode": "immediate",
                    "frame": {"duration": 0, "redraw": True}
                }],
                label=str(k)
            )
            for k in range(len(states))
        ]
    )]
)

st.plotly_chart(fig, use_container_width=True)

st.success("Bubble Sort Visualization Ready!")
st.write("Final Sorted Array:", arr)
