import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000/api";

function App() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    title: "",
    genres: "",
    actors: "",
    runtime_min: "",
    director: "",
    rating: "",
  });

  const [search, setSearch] = useState("");
  const [sortField, setSortField] = useState("title");
  const [sortDirection, setSortDirection] = useState("asc");

  // Fetch movies from backend (run once on mount)
  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true);
        setError("");
        const res = await fetch(`${API_BASE}/movies`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setMovies(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load movies.");
      } finally {
        setLoading(false);
      }
    };
    fetchMovies();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Filter + sort
  const filteredAndSortedMovies = () => {
    let result = [...movies];

    // Search by title
    if (search.trim() !== "") {
      const query = search.toLowerCase();
      result = result.filter((m) =>
        m.title.toLowerCase().includes(query)
      );
    }

    // Sort
    result.sort((a, b) => {
      const dir = sortDirection === "asc" ? 1 : -1;

      let av = a[sortField];
      let bv = b[sortField];

      if (sortField === "runtime_min" || sortField === "rating") {
        av = Number(av);
        bv = Number(bv);
      } else if (sortField === "genres" || sortField === "actors") {
        const aList = Array.isArray(av) ? av : av ? [av] : [];
        const bList = Array.isArray(bv) ? bv : bv ? [bv] : [];
        av = aList.join(", ");
        bv = bList.join(", ");
      }

      if (av < bv) return -1 * dir;
      if (av > bv) return 1 * dir;
      return 0;
    });

    return result;
  };

  const handleSort = (field) => {
    if (field === sortField) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const resetForm = () => {
    setForm({
      title: "",
      genres: "",
      actors: "",
      runtime_min: "",
      director: "",
      rating: "",
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!form.title || !form.rating) {
      setError("Title and Rating are required.");
      return;
    }
    
    const genreList = form.genres
      .split(",")
      .map((g) => g.trim())
      .filter((g) => g.length > 0);
    console.log(genreList);
    const actorList = form.actors
      .split(",")
      .map((a) => a.trim())
      .filter((a) => a.length > 0);

    const payload = {
      title: form.title,
      genres: genreList,
      actors: actorList,
      runtime_min: form.runtime_min ? Number(form.runtime_min) : null,
      director: form.director || null,
      rating: Number(form.rating),
    };

    try {
      const res = await fetch(`${API_BASE}/movies`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const saved = await res.json();
      setMovies((prev) => [...prev, saved]);
      resetForm();
    } catch (err) {
      console.error(err);
      setError("Failed to add movie.");
    }
  };

  const handleDelete = async (movieId) => {
    if (!movieId) return;

    try {
      const res = await fetch(`${API_BASE}/movies/${movieId}/`, {
        method: "DELETE",
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      setMovies((prev) => prev.filter((m) => m.movie_id !== movieId));
    } catch (err) {
      console.error(err);
      setError("Failed to delete movie.");
    }
  };

  const moviesToDisplay = filteredAndSortedMovies();

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>My Movie Library</h1>
        <p>Per-user movie displayer with rating, search, and sort.</p>
      </header>

      <main className="app-main">
        <section className="panel panel-form">
          <h2>Add a Movie</h2>
          <form onSubmit={handleSubmit} className="movie-form">
            <div className="form-row">
              <label>
                Title<span className="required">*</span>
              </label>
              <input
                type="text"
                name="title"
                value={form.title}
                onChange={handleFormChange}
                placeholder="Inception"
                required
              />
            </div>

            <div className="form-row">
              <label>Genres (comma-separated)</label>
              <input
                type="text"
                name="genres"
                value={form.genres}
                onChange={handleFormChange}
                placeholder="Sci-Fi, Action"
              />
            </div>

            <div className="form-row">
              <label>Actors (comma-separated)</label>
              <input
                type="text"
                name="actors"
                value={form.actors}
                onChange={handleFormChange}
                placeholder="Will Smith, Tom Hanks"
              />
            </div>

            <div className="form-row">
              <label>Runtime (min)</label>
              <input
                type="number"
                name="runtime_min"
                value={form.runtime_min}
                onChange={handleFormChange}
                placeholder="148"
              />
            </div>

            <div className="form-row">
              <label>Director</label>
              <input
                type="text"
                name="director"
                value={form.director}
                onChange={handleFormChange}
                placeholder="Steven Spielberg"
              />
            </div>

            <div className="form-row">
              <label>
                Rating (1–10)<span className="required">*</span>
              </label>
              <input
                type="number"
                min="1"
                max="10"
                step="0.1"
                name="rating"
                value={form.rating}
                onChange={handleFormChange}
                placeholder="8.7"
                required
              />
            </div>

            <button type="submit" className="btn primary">
              Add Movie
            </button>
          </form>

          {error && <p className="error-msg">{error}</p>}
        </section>

        <section className="panel panel-list">
          <div className="list-header">
            <h2>Movies</h2>
            <input
              type="text"
              className="search-input"
              placeholder="Search by title…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          {loading ? (
            <p>Loading movies…</p>
          ) : moviesToDisplay.length === 0 ? (
            <p>No movies yet.</p>
          ) : (
            <table className="movie-table">
              <thead>
                <tr>
                  <SortableHeader
                    label="Title"
                    field="title"
                    sortField={sortField}
                    sortDirection={sortDirection}
                    onSort={handleSort}
                  />
                  <SortableHeader
                    label="Genres"
                    field="genres"
                    sortField={sortField}
                    sortDirection={sortDirection}
                    onSort={handleSort}
                  />
                  <SortableHeader
                    label="Actors"
                    field="actors"
                    sortField={sortField}
                    sortDirection={sortDirection}
                    onSort={handleSort}
                  />
                  <SortableHeader
                    label="Runtime"
                    field="runtime_min"
                    sortField={sortField}
                    sortDirection={sortDirection}
                    onSort={handleSort}
                  />
                  <SortableHeader
                    label="Director"
                    field="director"
                    sortField={sortField}
                    sortDirection={sortDirection}
                    onSort={handleSort}
                  />
                  <SortableHeader
                    label="Rating"
                    field="rating"
                    sortField={sortField}
                    sortDirection={sortDirection}
                    onSort={handleSort}
                  />
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {moviesToDisplay.map((m) => (
                  <tr key={m.movie_id ?? `${m.title}-${m.rating}`}>
                    <td>{m.title}</td>
                    <td>
                      {Array.isArray(m.genre) ? m.genre.join(", ") : m.genre}
                    </td>
                    <td>
                      {Array.isArray(m.actors)
                        ? m.actors.join(", ")
                        : m.actors}
                    </td>
                    <td>{m.runtime_min}</td>
                    <td>{m.director}</td>
                    <td>{m.rating}</td>
                    <td>
                      <button
                        className="btn"
                        type="button"
                        onClick={() => handleDelete(m.movie_id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </div>
  );
}

function SortableHeader({ label, field, sortField, sortDirection, onSort }) {
  const isActive = sortField === field;
  const arrow = !isActive ? "⇅" : sortDirection === "asc" ? "↑" : "↓";

  return (
    <th
      onClick={() => onSort(field)}
      style={{ cursor: "pointer", whiteSpace: "nowrap" }}
    >
      {label} <span style={{ fontSize: "0.8rem" }}>{arrow}</span>
    </th>
  );
}

export default App;
