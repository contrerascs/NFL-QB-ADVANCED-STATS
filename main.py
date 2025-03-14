import streamlit as st
from helpers.data_loader import load_datasets

qb_complete_df = load_datasets()

print(qb_complete_df["Player"].unique())