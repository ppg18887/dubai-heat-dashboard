# Dubai urban heat dashboard on Streamlit

Your dashboard (`static/dashboard.html`) shown full width in a Streamlit app.
The open AI models (Qwen, Llama, Phi, Gemma, ...) run inside each visitor's own
browser, so the app needs **no GPU, no API key and almost no server memory**.

```
app.py                  the Streamlit app (shows the dashboard)
requirements.txt        streamlit only
.streamlit/config.toml  turns on static file serving
static/dashboard.html.gz.part01, part02   your dashboard, compressed and cut into pieces under 25 MB
split_dashboard.py      makes those pieces from a new dashboard file
add_open_models.py      adds the picker to a freshly generated dashboard
```

## Try it on your computer first

```bash
pip install -r requirements.txt
streamlit run app.py
```

It opens at http://localhost:8501.

## Put it online (free): Streamlit Community Cloud

1. **Create a GitHub account** (free) at github.com if you don't have one.
2. **Create a new repository**: click **New**, name it `dubai-heat`, choose **Public**, click **Create repository**.
3. **Upload the files.** Unzip this project. On the repository page click
   **Add file > Upload files** and drag in everything *inside* the `dubai_heat_streamlit`
   folder: `app.py`, `requirements.txt`, `README.md`, `add_open_models.py`, `split_dashboard.py`,
   the `static` folder and the `.streamlit` folder. Click **Commit changes**.
   - GitHub's web upload refuses any single file over **25 MB**. This project is prepared for that:
     the dashboard in `static/` is already compressed and cut into pieces
     (`dashboard.html.gz.part01`, `part02`), each under 25 MB. Upload **all** the pieces.
     The app joins and unpacks them by itself the first time it starts.
   - **Tip:** if dragging the `static` folder doesn't work in your browser, open the repository,
     click **Add file > Create new file**, type `static/x` in the name box to create the folder, then
     upload the pieces into it with **Add file > Upload files**.
   - Alternative: with **GitHub Desktop** or `git`, files up to 100 MB are accepted, so you can upload
     the plain `static/dashboard.html` (GitHub warns above 50 MB).
4. Go to **https://share.streamlit.io** and sign in with GitHub.
5. Click **Create app** and choose **Deploy a public app from GitHub**.
6. Pick your repository `dubai-heat`, branch `main`, and main file path `app.py`.
7. Click **Deploy**. The first build takes a minute or two.
8. When it opens, you have a public link ending in `.streamlit.app`. Share it.

## Updating the dashboard later

1. Generate the new dashboard from your Python pipeline.
2. Add the open models: `python add_open_models.py dubai_uhi_dashboard.html` (writes `dubai_uhi_dashboard_open_models.html`)
3. Cut it into upload-sized pieces: `python split_dashboard.py dubai_uhi_dashboard_open_models.html`
   (this rewrites the pieces in `static/`).
4. In the GitHub repository, replace the pieces in `static/` with the new ones (delete the old
   `dashboard.html.gz.part*` files first, in case the new file needs fewer pieces).
   Streamlit redeploys on its own.

## What visitors need

- A computer with **Chrome or Edge** for the in-browser AI models. The first use downloads a model
  (about 0.7 to 3.4 GB) once; after that it is cached.
- On phones, tablets or computers without a usable graphics card, choose
  **"No AI: built-in rules"** in the model list. Everything else still works.

## If something looks wrong

| Problem | Fix |
|---|---|
| The dashboard area is blank or shows code | The app switches to compatibility mode by itself. If it didn't, open the sidebar (arrow at top left) and turn on **Compatibility mode**, or add `?mode=embedded` to the link. |
| It opens slowly | Compatibility mode sends 45 MB through the app. Normal mode is faster. |
| The model list is greyed out | The browser can't use the graphics card. Use Chrome or Edge, or choose "No AI: built-in rules". |
| App is "sleeping" | Free apps sleep after a period without visitors. Click the wake-up button; it restarts in under a minute. |
| Build fails | Check that `requirements.txt` is in the repository root and contains `streamlit>=1.66.1`. |

## Good to know

- A **public** repository means your dashboard file is public too. A private repository works on
  Community Cloud for one app.
- Streamlit's documentation says its static file serving is meant for small files and that apps
  serving many or large files may hit resource limits. This app serves one file and does no
  computing, but if the host ever complains, move `static/dashboard.html` to GitHub Pages and
  embed it with the same `st.iframe(...)` line using its full `https://` address.
