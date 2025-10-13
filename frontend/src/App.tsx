import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { AllAccounts } from './pages/AllAccounts';
import { AccountDetails } from './pages/AccountDetails';
import { Admin } from './pages/Admin';
import { NewAccount } from './pages/NewAccount';
import { EditAccount } from './pages/EditAccount';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<AllAccounts />} />
          <Route path="accounts/new" element={<NewAccount />} />
          <Route path="accounts/:uid" element={<AccountDetails />} />
          <Route path="accounts/:uid/edit" element={<EditAccount />} />
          <Route path="admin" element={<Admin />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
