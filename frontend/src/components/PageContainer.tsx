import React from "react";

export default function PageContainer({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="bg-white min-h-screen max-h-fit flex flex-col py-16 2xl:px-96 xl:px-56 lg:px-44 md:px-24 px-8">
      {children}
    </div>
  );
}
