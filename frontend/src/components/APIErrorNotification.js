'use client';

import React from "react";
import useAPIError from "@/app/common/hooks/useAPIError";
import Modal from '@mui/material/Modal';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

function APIErrorNotification() {
  const { error, removeError } = useAPIError();

  const handleSubmit = () => {
    removeError();
  };

  return (
    <Modal
      open={!!error}
      style={style}
      data-testid="notification-modal"
    >
      <div>
        {error && error.message && <p>({error.message})</p>}
        <button data-testid="notification-submit-button" className="mt-2 bg-blue-500 text-white px-4 py-2 rounde" onClick={handleSubmit}>
          Ok
        </button>
      </div>
    </Modal>
  );
}

export default APIErrorNotification;
