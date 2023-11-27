import React from "react";

export default function PageContainer({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="bg-white min-h-screen max-h-fit flex flex-col py-16 px-96">
      {children}
    </div>
  );
}
