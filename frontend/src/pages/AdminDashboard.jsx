import React, { useState, useEffect } from "react";

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [activeTab, setActiveTab] = useState("users");
  const [loading, setLoading] = useState(true);
  const [editingUser, setEditingUser] = useState(null);
  const [editingPrediction, setEditingPrediction] = useState(null);
  const [showPredictionDetails, setShowPredictionDetails] = useState(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    const isAdmin = localStorage.getItem("isAdmin") === "true";
    if (!token || !isAdmin) {
      alert("Admin access required. Redirecting to admin login.");
      window.location.hash = "#/admin-login";
      return;
    }
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [usersRes, predictionsRes] = await Promise.all([
        fetch("http://localhost:8000/admin/users", {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch("http://localhost:8000/admin/predictions", {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      if (usersRes.ok) {
        const usersData = await usersRes.json();
        setUsers(usersData);
      }
      if (predictionsRes.ok) {
        const predictionsData = await predictionsRes.json();
        setPredictions(predictionsData);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Error loading data. Please check your connection.");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!confirm("Are you sure you want to delete this user?")) return;
    try {
      const response = await fetch(`http://localhost:8000/admin/users/${userId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        alert("User deleted successfully");
        fetchData();
      } else {
        alert("Failed to delete user");
      }
    } catch (error) {
      alert("Error deleting user");
    }
  };

  const handleDeletePrediction = async (predictionId) => {
    if (!confirm("Are you sure you want to delete this prediction?")) return;
    try {
      const response = await fetch(`http://localhost:8000/admin/predictions/${predictionId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        alert("Prediction deleted successfully");
        fetchData();
      } else {
        alert("Failed to delete prediction");
      }
    } catch (error) {
      alert("Error deleting prediction");
    }
  };

  const handleUpdateUser = async (userId, fullName, email) => {
    try {
      const response = await fetch(`http://localhost:8000/admin/users/${userId}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ full_name: fullName, email }),
      });
      if (response.ok) {
        alert("User updated successfully");
        setEditingUser(null);
        fetchData();
      } else {
        alert("Failed to update user");
      }
    } catch (error) {
      alert("Error updating user");
    }
  };

  const handleUpdatePrediction = async (predictionId, updates) => {
    try {
      const response = await fetch(`http://localhost:8000/admin/predictions/${predictionId}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updates),
      });
      if (response.ok) {
        alert("Prediction updated successfully");
        setEditingPrediction(null);
        fetchData();
      } else {
        alert("Failed to update prediction");
      }
    } catch (error) {
      alert("Error updating prediction");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("isAdmin");
    localStorage.removeItem("userName");
    window.location.hash = "#/";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white text-gray-900 flex items-center justify-center">
        <p className="text-xl">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white text-gray-900 font-poppins">
      {/* Navbar */}
      <nav className="bg-gray-100 border-b border-gray-200 px-8 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-red-500">🔐 Admin Dashboard</h1>
        <div className="flex gap-4">
          <button
            onClick={fetchData}
            className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg text-white"
          >
            Refresh
          </button>
          <button
            onClick={handleLogout}
            className="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-lg text-gray-900"
          >
            Logout
          </button>
        </div>
      </nav>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setActiveTab("users")}
          className={`px-8 py-4 font-semibold ${
            activeTab === "users"
              ? "bg-gray-100 text-blue-600 border-b-2 border-blue-600"
              : "text-gray-500 hover:text-gray-900"
          }`}
        >
          Users ({users.length})
        </button>
        <button
          onClick={() => setActiveTab("predictions")}
          className={`px-8 py-4 font-semibold ${
            activeTab === "predictions"
              ? "bg-gray-100 text-blue-600 border-b-2 border-blue-600"
              : "text-gray-500 hover:text-gray-900"
          }`}
        >
          Predictions ({predictions.length})
        </button>
      </div>

      {/* Content */}
      <div className="p-8">
        {activeTab === "users" && (
          <div className="bg-gray-100 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">All Users</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="p-3">ID</th>
                    <th className="p-3">Full Name</th>
                    <th className="p-3">Email</th>
                    <th className="p-3">Admin</th>
                    <th className="p-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id} className="border-b border-gray-200">
                      <td className="p-3">{user.id}</td>
                      <td className="p-3">
                        {editingUser?.id === user.id ? (
                          <input
                            type="text"
                            defaultValue={user.full_name}
                            onBlur={(e) => {
                              handleUpdateUser(user.id, e.target.value, user.email);
                            }}
                            className="bg-white px-2 py-1 rounded border border-gray-300"
                          />
                        ) : (
                          user.full_name
                        )}
                      </td>
                      <td className="p-3">
                        {editingUser?.id === user.id ? (
                          <input
                            type="email"
                            defaultValue={user.email}
                            onBlur={(e) => {
                              handleUpdateUser(user.id, user.full_name, e.target.value);
                            }}
                            className="bg-white px-2 py-1 rounded border border-gray-300"
                          />
                        ) : (
                          user.email
                        )}
                      </td>
                      <td className="p-3">{user.is_admin ? "✅" : "❌"}</td>
                      <td className="p-3">
                        <div className="flex gap-2">
                          <button
                            onClick={() =>
                              setEditingUser(editingUser?.id === user.id ? null : user)
                            }
                            className="bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded text-sm text-white"
                          >
                            {editingUser?.id === user.id ? "Cancel" : "Edit"}
                          </button>
                          <button
                            onClick={() => handleDeleteUser(user.id)}
                            className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded text-sm text-white"
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "predictions" && (
          <div className="bg-gray-100 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">All Predictions</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="p-3">ID</th>
                    <th className="p-3">User ID</th>
                    <th className="p-3">Career Domain</th>
                    <th className="p-3">Confidence</th>
                    <th className="p-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {predictions.map((pred) => (
                    <tr key={pred.id} className="border-b border-gray-200">
                      <td className="p-3">{pred.id}</td>
                      <td className="p-3">{pred.user_id}</td>
                      <td className="p-3">{pred.best_fit_career_domain}</td>
                      <td className="p-3">{(pred.confidence_score * 100).toFixed(1)}%</td>
                      <td className="p-3">
                        <div className="flex gap-2">
                          <button
                            onClick={() => setShowPredictionDetails(showPredictionDetails === pred.id ? null : pred.id)}
                            className="bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded text-sm text-white"
                          >
                            {showPredictionDetails === pred.id ? "Hide" : "View"}
                          </button>
                          <button
                            onClick={() => setEditingPrediction(editingPrediction?.id === pred.id ? null : pred)}
                            className="bg-yellow-500 hover:bg-yellow-600 px-3 py-1 rounded text-sm text-white"
                          >
                            {editingPrediction?.id === pred.id ? "Cancel" : "Edit"}
                          </button>
                          <button
                            onClick={() => handleDeletePrediction(pred.id)}
                            className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded text-sm text-white"
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {/* Prediction Details Modal */}
              {showPredictionDetails && predictions.find(p => p.id === showPredictionDetails) && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
                  <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
                    <h3 className="text-xl font-bold mb-4">Prediction Details</h3>
                    {(() => {
                      const pred = predictions.find(p => p.id === showPredictionDetails);
                      return (
                        <div className="space-y-3 text-sm">
                          <p><strong>ID:</strong> {pred.id}</p>
                          <p><strong>User ID:</strong> {pred.user_id}</p>
                          <p><strong>Career Domain:</strong> {pred.best_fit_career_domain}</p>
                          <p><strong>Confidence:</strong> {(pred.confidence_score * 100).toFixed(1)}%</p>
                          <p><strong>Rationale:</strong> {pred.career_rationale}</p>
                          <p><strong>Growth Roadmap:</strong> {pred.growth_roadmap}</p>
                          <p><strong>Skill Gap:</strong> {pred.skill_gap_analysis}</p>
                          <p><strong>Courses:</strong> {pred.recommended_courses}</p>
                          <p><strong>Backup Option:</strong> {pred.backup_career_option}</p>
                          <p><strong>Behavioral Insight:</strong> {pred.behavioral_insight}</p>
                        </div>
                      );
                    })()}
                    <button
                      onClick={() => setShowPredictionDetails(null)}
                      className="mt-4 bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded text-gray-900"
                    >
                      Close
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;

