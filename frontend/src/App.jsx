import { useEffect, useState } from "react";

// Adjust this if your backend runs somewhere else
const API_BASE = "http://localhost:8000/api";

function App() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    title: "",
    genre: "",
    release_year: "",
    runtime_min: "",
    production_country: "",
    rating: "",
  });

  const [search, setSearch] = useState("");
  const [sortField, setSortField] = useState("title");
  const [sortDirection, setSortDirection] = useState("asc"); // "asc" | "desc"

  // Fetch movies from backend
  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true);
        setError("");
        const res = await fetch(`${API_BASE}/movies`);
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
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
  }, []);

  // Helpers: sorting + filtering
  const filteredAndSortedMovies = () => {
    let result = [...movies];

    // Filter by search (title substring, case-insensitive)
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

      // Handle numbers vs strings
      if (sortField === "release_year" || sortField === "runtime_min" || sortField === "rating") {
        av = Number(av);
        bv = Number(bv);
      }

      if (av < bv) return -1 * dir;
      if (av > bv) return 1 * dir;
      return 0;
    });

    return result;
  };

  const handleSort = (field) => {
    if (field === sortField) {
      // toggle direction
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
      genre: "",
      release_year: "",
      runtime_min: "",
      production_country: "",
      rating: "",
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Basic validation
    if (!form.title || !form.release_year || !form.rating) {
      setError("Title, Release Year, and Rating are required.");
      return;
    }

    const payload = {
      title: form.title,
      genre: form.genre || null, // if you're also using MOVIE_GENRE, you can ignore this
      release_year: Number(form.release_year),
      runtime_min: form.runtime_min ? Number(form.runtime_min) : null,
      production_country: form.production_country || null,
      rating: Number(form.rating),
    };

    try {
      const res = await fetch(`${API_BASE}/movies`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const saved = await res.json();

      // Optimistically append to list
      setMovies((prev) => [...prev, saved]);
      resetForm();
    } catch (err) {
      console.error(err);
      setError("Failed to add movie.");
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
              <label>Genre</label>
              <input
                type="text"
                name="genre"
                value={form.genre}
                onChange={handleFormChange}
                placeholder="Sci-Fi"
              />
            </div>

            <div className="form-row">
              <label>
                Release Year<span className="required">*</span>
              </label>
              <input
                type="number"
                name="release_year"
                value={form.release_year}
                onChange={handleFormChange}
                placeholder="2010"
                required
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
              <label>Production Country</label>
              <input
                type="text"
                name="production_country"
                value={form.production_country}
                onChange={handleFormChange}
                placeholder="USA"
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
                    label="Genre"
                    field="genre"
                    sortField={sortField}
                    sortDirection={sortDirection}
                    onSort={handleSort}
                  />
                  <SortableHeader
                    label="Year"
                    field="release_year"
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
                    label="Country"
                    field="production_country"
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
                </tr>
              </thead>
              <tbody>
                {moviesToDisplay.map((m) => (
                  <tr key={m.movie_id ?? `${m.title}-${m.release_year}`}>
                    <td>{m.title}</td>
                    <td>{m.genre}</td>
                    <td>{m.release_year}</td>
                    <td>{m.runtime_min}</td>
                    <td>{m.production_country}</td>
                    <td>{m.rating}</td>
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
